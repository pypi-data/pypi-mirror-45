# -*- coding: utf-8 -*-
# run this to test the model

import argparse
import random
import os, time, datetime
import numpy as np
import torch.nn as nn
import torch.nn.init as init
import torch
from skimage.measure import compare_psnr
from skimage.io import imread, imsave
from get_patch import *
import segyio
from gain import *

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--set_dir', default='data', type=str, help='directory of test dataset')
    parser.add_argument('--set_names', default=['Test'], help='directory of test dataset')
    parser.add_argument('--rate', default=0.9, type=float, help='missing rate')
    parser.add_argument('--agc', default=True, type=bool, help='Agc operation of the data,True or False')
    parser.add_argument('--model_dir', default=os.path.join('models_inter', 'DnCNN_rate0.7'), help='directory of the model')
    parser.add_argument('--model_name', default='model.pth', type=str, help='the model name')
    parser.add_argument('--result_dir', default='results_inter', type=str, help='directory of test dataset')
    parser.add_argument('--save_result', default=1, type=int, help='save the denoised image, 1 or 0')
    return parser.parse_args()


def log(*args, **kwargs):
     print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S:"), *args, **kwargs)



def save_result(result, path):

    path = path if path.find('.') != -1 else path+'.png'
    ext = os.path.splitext(path)[-1]
    if ext in ('.txt', '.dlm'):
        np.savetxt(path, result, fmt='%2.4f')
    else:
        imsave(path, result)


def show(x, title=None, cbar=False, figsize=None):
    import matplotlib.pyplot as plt
    plt.figure(figsize=figsize)
    plt.imshow(x)
    if title:
        plt.title(title)
    if cbar:
        plt.colorbar()
    plt.show()
def compare_SNR(real_img,recov_img):
    real_mean = np.mean(real_img)
    tmp1 = real_img - real_mean
    real_var = sum(sum(tmp1*tmp1))

    noise = real_img - recov_img
    noise_mean = np.mean(noise)
    tmp2 = noise - noise_mean
    noise_var = sum(sum(tmp2*tmp2))

    if noise_var ==0 or real_var==0:
      s = 999.99
    else:
      s = 10*math.log(real_var/noise_var,10)
    return s

class DnCNN(nn.Module):

    def __init__(self, depth=17, n_channels=64, image_channels=1, use_bnorm=True, kernel_size=3):
        super(DnCNN, self).__init__()
        kernel_size = 3
        padding = 1
        layers = []
        layers.append(nn.Conv2d(in_channels=image_channels, out_channels=n_channels, kernel_size=kernel_size, padding=padding, bias=True))
        layers.append(nn.ReLU(inplace=True))
        for _ in range(depth-2):
            layers.append(nn.Conv2d(in_channels=n_channels, out_channels=n_channels, kernel_size=kernel_size, padding=padding, bias=False))
            layers.append(nn.BatchNorm2d(n_channels, eps=0.0001, momentum=0.95))
            layers.append(nn.ReLU(inplace=True))
        layers.append(nn.Conv2d(in_channels=n_channels, out_channels=image_channels, kernel_size=kernel_size, padding=padding, bias=False))
        self.dncnn = nn.Sequential(*layers)
        self._initialize_weights()

    def forward(self, x):
        out = self.dncnn(x)
        return out

    def _initialize_weights(self):
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                init.orthogonal_(m.weight)
                print('init weight')
                if m.bias is not None:
                    init.constant_(m.bias, 0)
            elif isinstance(m, nn.BatchNorm2d):
                init.constant_(m.weight, 1)
                init.constant_(m.bias, 0)


if __name__ == '__main__':

    args = parse_args()

    # model.load_state_dict(torch.load(os.path.join(args.model_dir, args.model_name)))
    model = torch.load(os.path.join(args.model_dir, args.model_name))
    log('load trained model')

    model.eval()  # evaluation mode
#    model.train()

    if torch.cuda.is_available():
        model = model.cuda()

    if not os.path.exists(args.result_dir):
        os.mkdir(args.result_dir)

    for set_cur in args.set_names:

        if not os.path.exists(os.path.join(args.result_dir, set_cur)):
            os.mkdir(os.path.join(args.result_dir, set_cur))
        psnrs = []
        SNRs = []

        for im in os.listdir(os.path.join(args.set_dir, set_cur)):
            if im.endswith(".segy") or im.endswith(".sgy"):
                filename = os.path.join(args.set_dir, set_cur, im)
                with segyio.open(filename,'r',ignore_geometry=True) as f:
                    f.mmap()
                    data = np.asarray([np.copy(x) for x in f.trace[0:1200]]).T
                    f.close()
                
                if args.agc:
                    data = gain(data,0.004,'agc',0.05,1)
                    
                # Select a small piece of data
                x = data[500:700,800:1000]
                mask = np.zeros(x.shape)
                TM = random.sample(range(x.shape[1]),round(args.rate*x.shape[1]))
                mask[:,TM] = 1
                mask = mask.astype(np.float32)
                y = x*mask
                y_ = torch.from_numpy(y).view(1, -1, y.shape[0], y.shape[1])


                torch.cuda.synchronize()
                start_time = time.time()
                y_ = y_.cuda()
                x_ = model(y_)  # inferences
                x_ = x_.view(y.shape[0], y.shape[1]) 
                x_ = x_.cpu()

                x_ = x_.detach().numpy().astype(np.float32)
                torch.cuda.synchronize()
                elapsed_time = time.time() - start_time
                print('%10s : %10s : %2.4f second' % (set_cur, im, elapsed_time))

                psnr_x_ = compare_psnr(x, x_)
                SNR_x_ = compare_SNR(x, x_)

                if args.save_result:

                    name, ext = os.path.splitext(im)
                    show(np.hstack((y, x_))) 
                    save_result(x_, path=os.path.join(args.result_dir, set_cur, name+'_dncnn'+'.png'))  # save simage
                psnrs.append(psnr_x_)
                SNRs.append(SNR_x_)

        psnr_avg = np.mean(psnrs)
        SNR_avg = np.mean(SNRs)

        psnrs.append(psnr_avg)
        SNRs.append(SNR_avg)
        if args.save_result:
            save_result(psnrs, path=os.path.join(args.result_dir, set_cur, 'results.txt'))
        log('Datset: {0:10s} \n  PSNR = {1:2.2f}dB, SNR = {2:1.4f}'.format(set_cur, psnr_avg, SNR_avg))








