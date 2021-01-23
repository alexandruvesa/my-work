# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 15:46:57 2021

@author: alexandru.vesa
"""
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()

def backbone(features):
  # Input layer
  input_layer = tf.reshape(features["x"], [-1, 40, 40, 3])
  #nput_layer = tf.reshape(vector, [-1, 40, 40, 3])

  # First convolutive layer
  conv1 = tf.compat.v1.layers.conv2d(inputs=input_layer, filters=16, kernel_size=[5, 5], padding="same", activation=tf.nn.relu)
  pool1 = tf.compat.v1.layers.max_pooling2d(inputs=conv1, pool_size=[2, 2], strides=2)

  # Second convolutive layer
  conv2 = tf.compat.v1.layers.conv2d(inputs=pool1, filters=48, kernel_size=[3, 3], padding="same", activation=tf.nn.relu)
  pool2 = tf.compat.v1.layers.max_pooling2d(inputs=conv2, pool_size=[2, 2], strides=2)
  
  # Third convolutive layer
  conv3 = tf.compat.v1.layers.conv2d(inputs=pool2, filters=64, kernel_size=[3, 3], padding="same", activation=tf.nn.relu)
  pool3 = tf.compat.v1.layers.max_pooling2d(inputs=conv3, pool_size=[2, 2], strides=2)
  
  # Fourth convolutive layer
  conv4 = tf.compat.v1.layers.conv2d(inputs=pool3, filters=64, kernel_size=[2, 2], padding="same", activation=tf.nn.relu)
  
  # Dense Layer
  flat = tf.reshape(conv4, [-1, 5 * 5 * 64])
  dense = tf.compat.v1.layers.dense(inputs=flat, units=100, activation=tf.nn.relu)
  
  return dense    


def single_head_cnn_model(features, labels, mode):
    dense = backbone(features)
    
    predictions = tf.compat.v1.layers.dense(inputs=dense, units =2)
    
    optimizer = tf.keras.optimizers.Adam()

    #Define te Head
    #regression_head = tf.estimator.RegressionHead(label_dimension = 2)
    #labels = labels[:, 2:8:5]
    
    print(labels)
    print(features)
    
    # regression_head.create_estimator_spec(features=features, mode=mode, logits=predictions, labels=labels, optimizer=optimizer)
    
    outputs = {
       "predictions": predictions
   }

   # We just want the predictions
    if mode == tf.estimator.ModeKeys.PREDICT:
          return tf.estimator.EstimatorSpec(mode=mode, predictions=outputs)
    
    # If not in mode.PREDICT, compute the loss (mean squared error)
    loss = tf.losses.mean_squared_error(labels=labels[:, 2:8:5], predictions=predictions)
    
    # Single optimization step
    if mode == tf.estimator.ModeKeys.TRAIN:
          optimizer = tf.train.AdamOptimizer()
          train_op = optimizer.minimize(loss=loss, global_step=tf.compat.v1.train.get_global_step())
          return tf.estimator.EstimatorSpec(mode=mode, loss=loss, train_op=train_op)
    
    # If not PREDICT or TRAIN, then we are evaluating the model
    eval_metric_ops = {
        "rmse": tf.metrics.RootMeanSquaredError(
            labels=labels, predictions=outputs["predictions"])}
    return tf.estimator.EstimatorSpec(
        mode=mode, loss=loss, eval_metric_ops=eval_metric_ops)