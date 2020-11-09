# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 14:05:57 2020

@author: alexandru.vesa
"""
from keras.models import Model
from keras.layers import Input, Dense, Flatten, Reshape, Lambda
from keras.layers import Conv2D, Add, ZeroPadding2D, MaxPooling2D, AveragePooling2D, GaussianNoise
from keras.layers.normalization import BatchNormalization
from keras.layers.advanced_activations import ReLU
from keras.initializers import TruncatedNormal, glorot_normal
from keras.regularizers import l2
from keras import backend as K
import tensorflow as tf
import numpy as np
import keras
from layers import UpsampleLike
from submodels import default_classification_model,default_regression_model , default_submodels, __build_model_pyramid , __build_pyramid


class AnchorParameters:
    """ The parameteres that define how anchors are generated.
    Args
        sizes   : List of sizes to use. Each size corresponds to one feature level.
        strides : List of strides to use. Each stride correspond to one feature level.
        ratios  : List of ratios to use per location in a feature map.
        scales  : List of scales to use per location in a feature map.
    """
    def __init__(self, sizes, strides, ratios, scales):
        self.sizes   = sizes
        self.strides = strides
        self.ratios  = ratios
        self.scales  = scales

    def num_anchors(self):
        return len(self.ratios) * len(self.scales)


"""
The default anchor parameters.
"""
AnchorParameters.default = AnchorParameters(
    sizes   = [32, 64, 128, 256, 512],
    strides = [8, 16, 32, 64, 128],
    ratios  = np.array([0.5, 1, 2], keras.backend.floatx()),
    scales  = np.array([2 ** 0, 2 ** (1.0 / 3.0), 2 ** (2.0 / 3.0)], keras.backend.floatx()),
)


class Network():

    def __init__(self,inputs):
        
        self.inputs=inputs

        self.WEIGHT_DECAY = 0.001
        self.model = self._create_model()

    def _res_block(self, x, filters_list, strides=1, use_bias=True, name=None):
        out = Conv2D(filters=filters_list[0],
                     kernel_size=1, strides=1,
                     use_bias=False,
                     kernel_initializer='glorot_normal', name='%s_1' % (name),
                     kernel_regularizer=l2(self.WEIGHT_DECAY))(x)
        out = BatchNormalization(name='%s_1_bn' % (name))(out)
        out = ReLU(name='%s_1_relu' % (name))(out)

        out = Conv2D(filters=filters_list[1],
                     kernel_size=3,
                     strides=1, padding='same',
                     use_bias=False,
                     kernel_initializer='glorot_normal',
                     name='%s_2' % (name), kernel_regularizer=l2(self.WEIGHT_DECAY))(out)
        out = BatchNormalization(name='%s_2_bn' % (name))(out)
        out = ReLU(name='%s_2_relu' % (name))(out)

        out = Conv2D(filters=filters_list[2],
                     kernel_size=1,
                     strides=1,
                     use_bias=False,
                     kernel_initializer='glorot_normal',
                     name='%s_3' % (name),
                     kernel_regularizer=l2(self.WEIGHT_DECAY))(out)
        out = BatchNormalization(name='%s_3_bn' % (name))(out)

        out = Add(name='%s_add' % (name))([x, out])
        out = ReLU(name='%s_relu' % (name))(out)
        return out

    def _res_block_proj(self, x, filters_list, strides=2, use_bias=True, name=None):
        '''
        y = f3(f2(f1(x))) + proj(x)
        '''
        out = Conv2D(filters=filters_list[0],
                     kernel_size=1,
                     strides=strides,
                     kernel_initializer='glorot_normal',
                     use_bias=False, name='%s_1' % (name))(x)
        out = BatchNormalization(name='%s_1_bn' % (name))(out)
        out = ReLU(name='%s_1_relu' % (name))(out)

        out = Conv2D(filters=filters_list[1],
                     kernel_size=3,
                     strides=1,
                     padding='same',
                     use_bias=False,
                     kernel_initializer='glorot_normal',
                     name='%s_2' % (name))(out)
        out = BatchNormalization(name='%s_2_bn' % (name))(out)
        out = ReLU(name='%s_2_relu' % (name))(out)

        out = Conv2D(filters=filters_list[2],
                     kernel_size=1, strides=1,
                     use_bias=False,
                     kernel_initializer='glorot_normal', name='%s_3' % (name))(out)
        out = BatchNormalization(name='%s_3_bn' % (name))(out)

        x = Conv2D(filters=filters_list[2],
                   kernel_size=1,
                   strides=strides,
                   use_bias=False,
                   kernel_initializer='glorot_normal', name='%s_proj' % (name))(x)
        x = BatchNormalization(name='%s_proj_bn' % (name))(x)

        out = Add(name='%s_add' % (name))([x, out])
        out = ReLU(name='%s_relu' % (name))(out)
        return out

    def _dilated_res_block(self, x, filters_list, strides=1, use_bias=True, name=None):
        '''
        y = f3(f2(f1(x))) + x
        '''
        out = Conv2D(filters=filters_list[0],
                     kernel_size=1,
                     strides=1, use_bias=False, kernel_initializer='glorot_normal', name='%s_1' % (name))(x)
        out = BatchNormalization(name='% s_1_bn' % (name))(out)
        out = ReLU(name='%s_1_relu' % (name))(out)

        out = Conv2D(filters=filters_list[1],
                     kernel_size=3,
                     strides=1,
                     padding='same',
                     dilation_rate=2, use_bias=False, kernel_initializer='glorot_normal', name='%s_2' % (name))(out)
        out = BatchNormalization(name='%s_2_bn' % (name))(out)
        out = ReLU(name='%s_2_relu' % (name))(out)

        out = Conv2D(filters=filters_list[2],
                     kernel_size=1,
                     strides=1, use_bias=False, kernel_initializer='glorot_normal', name='%s_3' % (name))(out)
        out = BatchNormalization(name='%s_3_bn' % (name))(out)

        out = Add(name='%s_add' % (name))([x, out])
        out = ReLU(name='%s_relu' % (name))(out)
        return out

    def _dilated_res_block_proj(self, x, filters_list, strides=1, use_bias=True, name=None):
        '''
        y = f3(f2(f1(x))) + proj(x)
        '''
        out = Conv2D(filters=filters_list[0],
                     kernel_size=1, strides=1,
                     use_bias=False,
                     kernel_initializer='glorot_normal',
                     name='%s_1' % (name), kernel_regularizer=l2(self.WEIGHT_DECAY))(x)
        out = BatchNormalization(name='%s_1_bn' % (name))(out)
        out = ReLU(name='%s_1_relu' % (name))(out)

        out = Conv2D(filters=filters_list[1],
                     kernel_size=3,
                     strides=1, padding='same',
                     dilation_rate=2,
                     use_bias=False,
                     kernel_initializer='glorot_normal',
                     name='%s_2' % (name), kernel_regularizer=l2(self.WEIGHT_DECAY))(out)
        out = BatchNormalization(name='%s_2_bn' % (name))(out)
        out = ReLU(name='%s_2_relu' % (name))(out)

        out = Conv2D(filters=filters_list[2],
                     kernel_size=1, strides=1, use_bias=False,
                     kernel_initializer='glorot_normal', name='%s_3' % (name),
                     kernel_regularizer=l2(self.WEIGHT_DECAY))(out)
        out = BatchNormalization(name='%s_3_bn' % (name))(out)

        x = Conv2D(filters=filters_list[2],
                   kernel_size=1,
                   strides=1, use_bias=False,
                   kernel_initializer='glorot_normal',
                   name='%s_proj' % (name), kernel_regularizer=l2(self.WEIGHT_DECAY))(x)
        x = BatchNormalization(name='%s_proj_bn' % (name))(x)

        out = Add(name='%s_add' % (name))([x, out])
        out = ReLU(name='%s_relu' % (name))(out)
        return out

    def _resnet_body(self, x, filters_list, num_blocks, strides=2, name=None):
        out = self._res_block_proj(x=x, filters_list=filters_list, strides=strides, name='%s_1' % (name))
        for i in range(1, num_blocks):
            out = self._res_block(x=out, filters_list=filters_list, name='%s_%s' % (name, str(i + 1)))
        return out

    def _detnet_body(self, x, filters_list, num_blocks, strides=1, name=None):
        out = self._dilated_res_block_proj(x=x, filters_list=filters_list, name='%s_1' % (name))
        for i in range(1, num_blocks):
            out = self._dilated_res_block(x=out, filters_list=filters_list, name='%s_%s' % (name, str(i + 1)))
        return out

    def _create_model(self):
        filters_list = [[64],
                        [64, 64, 256],
                        [128, 128, 512],
                        [256, 256, 1024],
                        [256, 256, 256],
                        [256, 256, 256]]
        blocks_list = [1, 3, 4, 6, 3, 3]
        # stage 1
        #inputs = Input(shape=(512, 640, 3), name='inputs')

        inputs_pad = ZeroPadding2D(padding=3, name='inputs_pad')(self.inputs)
        gauss1 = GaussianNoise(0.1)(inputs_pad)

        conv1 = Conv2D(filters=filters_list[0][0], kernel_size=7,
                       strides=2, use_bias=False, name='conv1')(gauss1)
        conv1 = BatchNormalization(name='conv1_bn')(conv1)
        conv1 = ReLU(name='conv1_relu')(conv1)

        # stage 2
        conv1_pad = ZeroPadding2D(padding=1, name='conv1_pad')(conv1)
        conv1_pool = MaxPooling2D(
            pool_size=3, strides=2, name='conv1_maxpool')(conv1_pad)
        conv2_x = self._resnet_body(
            x=conv1_pool, filters_list=filters_list[1], num_blocks=blocks_list[1], strides=1, name='res2')

        # stage 3
        conv3_x = self._resnet_body(
            x=conv2_x, filters_list=filters_list[2], num_blocks=blocks_list[2], strides=2, name='res3')

        # stage 4
        conv4_x = self._resnet_body(
            x=conv3_x, filters_list=filters_list[3], num_blocks=blocks_list[3], strides=2, name='res4')

        # stage 5
        conv5_x = self._detnet_body(
            x=conv4_x, filters_list=filters_list[4], num_blocks=blocks_list[4], strides=1, name='dires5')

        # stage 6
        final_convolution = self._detnet_body(
            x=conv5_x, filters_list=filters_list[5], num_blocks=blocks_list[5], strides=1, name='dires6')

      

        # reshape
        #pred_reshaped = Reshape((self.config.ANCHORS, -1))(final_layer)

        #pred_padded = Lambda(self._pad)(pred_reshaped)
        model = Model(inputs=self.inputs, outputs=final_convolution)
        model.summary()

        return model

    def _pad(self, input):
        """
        pads the network output so y_pred and y_true have the same dimensions
        :param input: previous layer
        :return: layer, last dimensions padded for 4
        """

        padding = np.zeros((3, 2))
        padding[2, 1] = 4
        return tf.pad(input, padding, "CONSTANT")
    
    
    
def __create_pyramid_features(backbone_layers, pyramid_levels, feature_size=256):
    """ Creates the FPN layers on top of the backbone features.
    Args
        backbone_layers: a dictionary containing feature stages C3, C4, C5 from the backbone. Also contains C2 if provided.
        pyramid_levels: Pyramid levels in use.
        feature_size : The feature size to use for the resulting feature levels.
    Returns
        output_layers : A dict of feature levels. P3, P4, P5, P6 are always included. P2, P6, P7 included if in use.
    """

    output_layers = {}

    # upsample C5 to get P5 from the FPN paper
    P5           = keras.layers.Conv2D(feature_size, kernel_size=1, strides=1, padding='same', name='C5_reduced')(backbone_layers['C5'])
    P5_upsampled = UpsampleLike(name='P5_upsampled')([P5, backbone_layers['C4']])
    P5           = keras.layers.Conv2D(feature_size, kernel_size=3, strides=1, padding='same', name='P5')(P5)
    output_layers["P5"] = P5

    # add P5 elementwise to C4
    P4           = keras.layers.Conv2D(feature_size, kernel_size=1, strides=1, padding='same', name='C4_reduced')(backbone_layers['C4'])
    P4           = keras.layers.Add(name='P4_merged')([P5_upsampled, P4])
    P4_upsampled = UpsampleLike(name='P4_upsampled')([P4, backbone_layers['C3']])
    P4           = keras.layers.Conv2D(feature_size, kernel_size=3, strides=1, padding='same', name='P4')(P4)
    output_layers["P4"] = P4

    # add P4 elementwise to C3
    P3 = keras.layers.Conv2D(feature_size, kernel_size=1, strides=1, padding='same', name='C3_reduced')(backbone_layers['C3'])
    P3 = keras.layers.Add(name='P3_merged')([P4_upsampled, P3])
    if 'C2' in backbone_layers and 2 in pyramid_levels:
        P3_upsampled = UpsampleLike(name='P3_upsampled')([P3, backbone_layers['C2']])
    P3 = keras.layers.Conv2D(feature_size, kernel_size=3, strides=1, padding='same', name='P3')(P3)
    output_layers["P3"] = P3

    if 'C2' in backbone_layers and 2 in pyramid_levels:
        P2 = keras.layers.Conv2D(feature_size, kernel_size=1, strides=1, padding='same', name='C2_reduced')(backbone_layers['C2'])
        P2 = keras.layers.Add(name='P2_merged')([P3_upsampled, P2])
        P2 = keras.layers.Conv2D(feature_size, kernel_size=3, strides=1, padding='same', name='P2')(P2)
        output_layers["P2"] = P2

    # "P6 is obtained via a 3x3 stride-2 conv on C5"
    if 6 in pyramid_levels:
        P6 = keras.layers.Conv2D(feature_size, kernel_size=3, strides=2, padding='same', name='P6')(backbone_layers['C5'])
        output_layers["P6"] = P6

    # "P7 is computed by applying ReLU followed by a 3x3 stride-2 conv on P6"
    if 7 in pyramid_levels:
        if 6 not in pyramid_levels:
            raise ValueError("P6 is required to use P7")
        P7 = keras.layers.Activation('relu', name='C6_relu')(P6)
        P7 = keras.layers.Conv2D(feature_size, kernel_size=3, strides=2, padding='same', name='P7')(P7)
        output_layers["P7"] = P7

    return output_layers



def retinanet(
    inputs,
    backbone_layers,
    num_classes,
    num_anchors             = None,
    create_pyramid_features = __create_pyramid_features,
    pyramid_levels          = None,
    submodels               = None,
    name                    = 'retinanet'
):
    """ Construct a RetinaNet model on top of a backbone.
    This model is the minimum model necessary for training (with the unfortunate exception of anchors as output).
    Args
        inputs                  : keras.layers.Input (or list of) for the input to the model.
        num_classes             : Number of classes to classify.
        num_anchors             : Number of base anchors.
        create_pyramid_features : Functor for creating pyramid features given the features C3, C4, C5, and possibly C2 from the backbone.
        pyramid_levels          : pyramid levels to use.
        submodels               : Submodels to run on each feature map (default is regression and classification submodels).
        name                    : Name of the model.
    Returns
        A keras.models.Model which takes an image as input and outputs generated anchors and the result from each submodel on every pyramid level.
        The order of the outputs is as defined in submodels:
        ```
        [
            regression, classification, other[0], other[1], ...
        ]
        ```
    """

    if num_anchors is None:
        num_anchors = AnchorParameters.default.num_anchors()

    if submodels is None:
        submodels = default_submodels(num_classes, num_anchors)

    if pyramid_levels is None:
        pyramid_levels = [3, 4, 5, 6, 7]

    if 2 in pyramid_levels and 'C2' not in backbone_layers:
        raise ValueError("C2 not provided by backbone model. Cannot create P2 layers.")

    if 3 not in pyramid_levels or 4 not in pyramid_levels or 5 not in pyramid_levels:
        raise ValueError("pyramid levels 3, 4, and 5 required for functionality")

    # compute pyramid features as per https://arxiv.org/abs/1708.02002
    features = create_pyramid_features(backbone_layers, pyramid_levels)
    feature_list = [features['P{}'.format(p)] for p in pyramid_levels]

    # for all pyramid levels, run available submodels
    pyramids = __build_pyramid(submodels, feature_list)

    return keras.models.Model(inputs=inputs, outputs=pyramids, name=name)

inputs = keras.layers.Input(shape=(512, 640, 3))

detnet = Network(inputs)
detnet=detnet.model



layer_outputs=[
    detnet.get_layer('dires6_3_relu').output,
    detnet.get_layer('dires5_3_relu').output,
    detnet.get_layer('res4_6_relu').output,
    detnet.get_layer('res3_4_relu').output]

detnet = keras.models.Model(inputs=inputs, outputs=layer_outputs)


backbone_layers = {
    'C5': detnet.outputs[0],
    'C4':detnet.outputs[1],
    'C3':detnet.outputs[2],
    'C2':detnet.outputs[3]}


output_layers = __create_pyramid_features(backbone_layers, pyramid_levels = [3,4,5,6,7])

retina = retinanet(inputs, backbone_layers, 2)

#retina.save('retina.h5')
