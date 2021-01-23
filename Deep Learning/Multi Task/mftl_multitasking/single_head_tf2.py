import tensorflow as tf
from tensorflow.keras.layers import Conv2D, MaxPool2D, Dense


def backbone(features):
  # Input layer
  input_layer = tf.reshape(features["x"], [-1, 40, 40, 3])
  #nput_layer = tf.reshape(vector, [-1, 40, 40, 3])

  # First convolutive layer
  conv1 = tf.keras.layers.Convolution2D( filters=16, kernel_size=[5, 5], padding="same", activation=tf.nn.relu)(input_layer)
  pool1 = tf.keras.layers.MaxPooling2D(pool_size=[2, 2], strides=2)(conv1)

  # Second convolutive layer
  conv2 = tf.keras.layers.Convolution2D (filters=48, kernel_size=[3, 3], padding="same", activation=tf.nn.relu)(pool1)
  pool2 = tf.keras.layers.MaxPooling2D(pool_size=[2, 2], strides=2)(conv2)
  
  # Third convolutive layer
  conv3 = tf.keras.layers.Convolution2D(filters=64, kernel_size=[3, 3], padding="same", activation=tf.nn.relu)(pool2)
  pool3 = tf.keras.layers.MaxPooling2D( pool_size=[2, 2], strides=2)(conv3)
  
  # Fourth convolutive layer
  conv4 = tf.keras.layers.Convolution2D( filters=64, kernel_size=[2, 2], padding="same", activation=tf.nn.relu)(pool3)
  
  # Dense Layer
  flat = tf.reshape(conv4, [-1, 5 * 5 * 64])
  dense = Dense( units=100, activation=tf.nn.relu)(flat)
  
  return dense    


def single_head_cnn_model_tf2(features, labels, mode):
    dense = backbone(features)
    
    predictions = tf.keras.layers.Dense(units =2)(dense)
    
    optimizer = tf.keras.optimizers.Adam()

    #Define te Head
    regression_head = tf.estimator.RegressionHead(label_dimension = 2)
    #labels = labels[:, 2:8:5]
    
    print(labels)
    print(features)
    
    return regression_head.create_estimator_spec(
        features=features,
        labels=labels[:, 2:8:5],
        mode=tf.estimator.ModeKeys.TRAIN,
        trainable_variables= tf.compat.v1.trainable_variables(),
        logits=predictions,
        optimizer=optimizer)