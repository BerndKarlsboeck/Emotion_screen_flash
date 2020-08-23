from __future__ import print_function
import keras
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Dense,Dropout,Activation,Flatten,BatchNormalization
from keras.layers import Conv2D,MaxPooling2D
from keras.optimizers import RMSprop,SGD,Adam
from keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
import os

###########################################################
# Defining, normalizing and augmenting training data + validation data
###########################################################

num_classes = 7
img_rows, img_cols = 48, 48
batch_size = 32

###########################################################
# Defining, normalizing and augmenting training data + validation data
###########################################################

# make sure to add correct path to training and validation data
train_data_dir = r'C:\Users\...YOURPATH...\Emotion_screen_flash\images\images\train'
validation_data_dir = r'C:\Users\...YOURPATH...\Emotion_screen_flash\images\images\validation'

train_datagen = ImageDataGenerator(
					rescale = 1./255,
					rotation_range = 30,
					shear_range = 0.3,
					zoom_range = 0.3,
					width_shift_range = 0.4,
					height_shift_range = 0.4,
					horizontal_flip = True,
					fill_mode = 'nearest')

validation_datagen = ImageDataGenerator(rescale = 1./255)

train_generator = train_datagen.flow_from_directory(
					train_data_dir,
					color_mode = 'grayscale',
					target_size = (img_rows,img_cols),
					batch_size = batch_size,
					class_mode = 'categorical',
					shuffle = True)

validation_generator = validation_datagen.flow_from_directory(
							validation_data_dir,
							color_mode = 'grayscale',
							target_size = (img_rows,img_cols),
							batch_size = batch_size,
							class_mode = 'categorical',
							shuffle = True)

###########################################################
# Defining model architecture
###########################################################

model = Sequential()

# 1

model.add(Conv2D(32, (3, 3), padding = 'same', kernel_initializer = 'he_normal', input_shape = (img_rows, img_cols, 1)))
model.add(Activation('elu'))
model.add(BatchNormalization())
model.add(Conv2D(32, (3, 3), padding = 'same', kernel_initializer = 'he_normal', input_shape = (img_rows, img_cols, 1)))
model.add(Activation('elu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size = (2, 2)))
model.add(Dropout(0.2))

# 2

model.add(Conv2D(64, (3, 3), padding = 'same', kernel_initializer = 'he_normal'))
model.add(Activation('elu'))
model.add(BatchNormalization())
model.add(Conv2D(64, (3, 3), padding = 'same', kernel_initializer = 'he_normal'))
model.add(Activation('elu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size = (2, 2)))
model.add(Dropout(0.2))

# 3

model.add(Conv2D(128, (3, 3), padding = 'same', kernel_initializer = 'he_normal'))
model.add(Activation('elu'))
model.add(BatchNormalization())
model.add(Conv2D(128, (3,3), padding = 'same', kernel_initializer = 'he_normal'))
model.add(Activation('elu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size = (2, 2)))
model.add(Dropout(0.2))

# 4

model.add(Conv2D(256, (3, 3), padding = 'same', kernel_initializer = 'he_normal'))
model.add(Activation('elu'))
model.add(BatchNormalization())
model.add(Conv2D(256, (3, 3), padding = 'same', kernel_initializer = 'he_normal'))
model.add(Activation('elu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size = (2, 2)))
model.add(Dropout(0.2))

# 5

model.add(Flatten())
model.add(Dense(64, kernel_initializer = 'he_normal'))
model.add(Activation('elu'))
model.add(BatchNormalization())
model.add(Dropout(0.5))

# 6

model.add(Dense(64, kernel_initializer = 'he_normal'))
model.add(Activation('elu'))
model.add(BatchNormalization())
model.add(Dropout(0.5))

# 7

model.add(Dense(num_classes, kernel_initializer = 'he_normal'))
model.add(Activation('softmax'))

# uncomment the line below to see he CNN network summary printed
# print(model.summary())

###########################################################
# Defining model saving after training and all training checkpoints
###########################################################

checkpoint = ModelCheckpoint('Emotion_recognition_model.h5',
                             monitor = 'val_loss',
                             mode = 'min',
                             save_best_only = True,
                             verbose = 1)

earlystop = EarlyStopping(monitor = 'val_loss',
                          min_delta = 0,
                          patience = 3,
                          verbose = 1,
                          restore_best_weights = True
                          )

reduce_lr = ReduceLROnPlateau(monitor = 'val_loss',
                              factor = 0.2,
                              patience = 3,
                              verbose = 1,
                              min_delta = 0.0001)

callbacks = [earlystop, checkpoint, reduce_lr]

###########################################################
# Compiling model
###########################################################

model.compile(loss = 'categorical_crossentropy',
              optimizer = Adam(lr = 0.001),
              metrics = ['accuracy'])

nb_train_samples = 28821
nb_validation_samples = 7066
epochs = 25

###########################################################
# Training model
###########################################################

history=model.fit(
                train_generator,
                steps_per_epoch = nb_train_samples//batch_size,
                epochs = epochs,
                callbacks = callbacks,
                validation_data = validation_generator,
                validation_steps = nb_validation_samples//batch_size)
