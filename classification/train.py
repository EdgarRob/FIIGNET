from fastai.vision.all import *
from fastai.vision.augment import FlipItem
import os
import argparse

# python train.py --input_path '/path/to/image/directory' --output_path '/path/to/learner.pkl'

def main(args):
    path = args.input_path

    data = ImageDataLoaders.from_folder(path, train=".", valid_pct=0.2, 
                                        item_tfms=Resize(460),
                                        batch_tfms=[*aug_transforms(size=224, min_scale=0.75), 
                                                    Normalize.from_stats(*imagenet_stats),
                                                    FlipItem(p=0.5)])

    learn = cnn_learner(data, resnet152, metrics=accuracy)

    learn.lr_find()

    learn.recorder.plot_lr_find()

    lr = 1e-4

    learn.fit_one_cycle(4, slice(lr))

    learn.unfreeze()
    learn.fit_one_cycle(30, slice(lr/100, lr))

    interp = ClassificationInterpretation.from_learner(learn)
    interp.plot_confusion_matrix()

    learn.export(args.output_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Train a CNN for image classification.')
    parser.add_argument('--input_path', type=str, required=True, help='Input path for images')
    parser.add_argument('--output_path', type=str, required=True, help='Output path for the model')
    
    args = parser.parse_args()

    main(args)
