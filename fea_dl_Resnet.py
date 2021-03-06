# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 18:55:21 2019

@author: xngu0004
"""

import numpy as np
import random
import scipy.io as sio
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.utils import shuffle
from sklearn.preprocessing import LabelEncoder
from keras import regularizers
from keras.layers import Input, Dense, GlobalAveragePooling1D
from keras.callbacks import ModelCheckpoint
from keras.layers import Conv1D, BatchNormalization, Activation
from keras.layers import LSTM, add
from keras.models import Model
from keras.optimizers import Adam
from keras.utils import to_categorical
import keras.backend as K
from keras.callbacks import Callback
from keras.callbacks import EarlyStopping
from sklearn import svm

#####################################################
"Select a configuration"

list_skill = ["Suture","Knot","Needle"]
win = [90,120,150,180]
over = [30,60]

#####################################################

####################################################
for skill in list_skill:
    for tim in range(1,6):
        acc_1 = []
        accu = 0
        acc_1_fea = []
        accu_fea = 0
        # users in Group
        novice = ['B', 'G', 'H', 'I']
        intermediate = ['C', 'F']
        expert = ['D', 'E']

        " Load the data"
        " Reading the data "
        print('loading the dataset')
        dataset = sio.loadmat('../data/'+skill+'_dataX_basic_'+str(win)+'_'+str(over)+'.mat')

        features = dataset['dataX']
        sizeD_ts = (((features[0,0:1])[0])[0,:])[0].shape[0]
        sizeD_va = (((features[0,0:1])[0])[0,:])[0].shape[1]
        print('loaded the dataset')
    
        ###############################################################################

        print('Pre-process data')
        for user in range(1,6):

            " Initialize data for concatenation "
            X_test1 = np.ones((1,sizeD_ts,sizeD_va))
            y_test1 = np.ones(1)
            X_train1 = np.ones((1,sizeD_ts,sizeD_va))
            y_train1 = np.ones(1)

            # Extract data for training and testing
            for j in range(0,3): # 3 means 3 groups
                for i in range(0, (((features[0,j:j+1])[0])[0,:]).shape[0]):
                    k = (((features[0,j:j+1])[0])[2,:])[i]
                    if (k == user): # take out the ith trial of each user for testing
                        temp_x = (((features[0,j:j+1])[0])[0,:])[i]
                        temp_x1 = temp_x.reshape(1,sizeD_ts,sizeD_va)
                        X_test1 = np.concatenate((X_test1, temp_x1), axis=0) 
                        user_temp = (((features[0,j:j+1])[0])[1,:])[i]
        
                        if(user_temp in novice):
                            y_test1 = np.concatenate((y_test1,[0]))
                        elif(user_temp in intermediate):
                            y_test1 = np.concatenate((y_test1,[1]))
                        elif(user_temp in expert):
                            y_test1 = np.concatenate((y_test1,[2]))
                    else:
                        temp_x = (((features[0,j:j+1])[0])[0,:])[i]
                        temp_x1 = temp_x.reshape(1,sizeD_ts,sizeD_va)
                        X_train1 = np.concatenate((X_train1, temp_x1), axis=0)
                        user_temp = (((features[0,j:j+1])[0])[1,:])[i]
        
                        if(user_temp in novice):
                            y_train1 = np.concatenate((y_train1,[0]))
                        elif(user_temp in intermediate):
                            y_train1 = np.concatenate((y_train1,[1]))
                        elif(user_temp in expert):
                            y_train1 = np.concatenate((y_train1,[2]))
        
            " Delete the first column "
            X_test1 = np.delete(X_test1,np.s_[0:1], axis=0)
            y_test1 = np.delete(y_test1,np.s_[0:1])
            X_train1 = np.delete(X_train1,np.s_[0:1], axis=0)
            y_train1 = np.delete(y_train1,np.s_[0:1])

            " Shuffle the training and testing data "
            X_test, y_test = shuffle(X_test1, y_test1, random_state = random.randint(10,50))
            X_train, y_train = shuffle(X_train1, y_train1, random_state = random.randint(10,50))
    
            classes = np.unique(y_train)
            le = LabelEncoder()
            y_ind = le.fit_transform(y_train.ravel())
            recip_freq = len(y_train) / (len(le.classes_) * np.bincount(y_ind).astype(np.float64))
            class_weight = recip_freq[le.transform(classes)]
    
            " One-hot coding"
            labels_train = to_categorical(y_train)
            labels_test = to_categorical(y_test)

            ###########################################################################
            print("Ready to train")
            #model = model_arch2(withOP=True)
            
            #######-------- CNN -------------
#            ip = Input(shape=(sizeD_ts, sizeD_va), name='main_input')
#    
#            x = Conv1D(16, 7, padding='same', kernel_initializer='he_uniform')(ip)
#            x = BatchNormalization()(x)
#            x = Activation('relu')(x)
#
#            x = Conv1D(32, 5, padding='same', kernel_initializer='he_uniform')(x)
#            x = BatchNormalization()(x)
#            x = Activation('relu')(x)
#            fea = GlobalAveragePooling1D()(x)
#
#            out = Dense(3, kernel_regularizer=regularizers.l2(0.001), activation='softmax')(fea)
#
#            model = Model(ip, out)
#            #model.summary()

#            #######----------LSTM-----------
#            ip = Input(shape=(sizeD_ts, sizeD_va), name='main_input')
#    
#            x = LSTM(32, return_sequences=True)(ip)
#            fea = LSTM(32)(x)
#
#            out = Dense(3, kernel_regularizer=regularizers.l2(0.001), activation='softmax')(fea)
#
#            model = Model(ip, out)
#            #model.summary()

#            #######---------CNN+LSTM------------
#            ip = Input(shape=(sizeD_ts, sizeD_va), name='main_input')
#    
#            x = Conv1D(16, 7, padding='same', kernel_initializer='he_uniform')(ip)
#            x = BatchNormalization()(x)
#            x = Activation('relu')(x)
#
#            x = Conv1D(32, 5, padding='same', kernel_initializer='he_uniform')(x)
#            x = BatchNormalization()(x)
#            x = Activation('relu')(x)
#    
#            x = LSTM(32, return_sequences=True)(x)
#            fea = LSTM(32)(x)
#
#            out = Dense(3, kernel_regularizer=regularizers.l2(0.001), activation='softmax')(fea)
#            
#            model = Model(ip, out)
#            #model.summary()
            
            #######---------Resnet------------
            ip = Input(shape=(sizeD_ts, sizeD_va), name='main_input')
    
            ##### Block 1
            x1 = Conv1D(64, 8, padding='same', kernel_initializer='he_uniform')(ip)
            x1 = BatchNormalization()(x1)
            x1 = Activation('relu')(x1)
            
            x2 = Conv1D(64, 5, padding='same', kernel_initializer='he_uniform')(x1)
            x2 = BatchNormalization()(x2)
            x2 = Activation('relu')(x2)
            
            x3 = Conv1D(64, 3, padding='same', kernel_initializer='he_uniform')(x2)
            x3 = BatchNormalization()(x3)

            # expand channels for the sum
            sx2 = Conv1D(64, 1, padding='same', kernel_initializer='he_uniform')(ip)
            sx2 = BatchNormalization()(sx2)
            
            outputB1 = add([sx2, x3])
            outputB1 = Activation('relu')(outputB1)
            
            ##### Block 2
            x1 = Conv1D(64, 8, padding='same', kernel_initializer='he_uniform')(outputB1)
            x1 = BatchNormalization()(x1)
            x1 = Activation('relu')(x1)
            
            x2 = Conv1D(64, 5, padding='same', kernel_initializer='he_uniform')(x1)
            x2 = BatchNormalization()(x2)
            x2 = Activation('relu')(x2)
            
            x3 = Conv1D(64, 3, padding='same', kernel_initializer='he_uniform')(x2)
            x3 = BatchNormalization()(x3)

            # expand channels for the sum
            sx2 = Conv1D(64, 1, padding='same', kernel_initializer='he_uniform')(outputB1)
            sx2 = BatchNormalization()(sx2)
            
            outputB2 = add([sx2, x3])
            outputB2 = Activation('relu')(outputB2)
            
            ##### Block 3
            x1 = Conv1D(64, 8, padding='same', kernel_initializer='he_uniform')(outputB2)
            x1 = BatchNormalization()(x1)
            x1 = Activation('relu')(x1)
            
            x2 = Conv1D(64, 5, padding='same', kernel_initializer='he_uniform')(x1)
            x2 = BatchNormalization()(x2)
            x2 = Activation('relu')(x2)
            
            x3 = Conv1D(64, 3, padding='same', kernel_initializer='he_uniform')(x2)
            x3 = BatchNormalization()(x3)

            #do not need to expand channels for the sum
            sx2 = BatchNormalization()(outputB2)
            
            outputB3 = add([sx2, x3])
            outputB3 = Activation('relu')(outputB2)
            
            #### End
            fea = GlobalAveragePooling1D()(outputB3)
            out = Dense(3, kernel_regularizer=regularizers.l2(0.001), activation='softmax')(fea)
            
            model = Model(ip, out)
            #model.summary()
######---------------------
            
            epochs_s = 100
            batch_s = 16
            learning_rate = 1e-3   
            weight_fn = "./weights/weights_fea_Resnet_t"+str(user)+".h5"
            model_checkpoint = ModelCheckpoint(weight_fn, verbose=1, mode='max', monitor='val_acc', save_best_only=True, save_weights_only=True)
            stop = EarlyStopping(monitor='val_loss', patience=15)
            callback_list = [model_checkpoint, stop]
            optm = Adam(lr=learning_rate)

            model.compile(optimizer=optm, loss='categorical_crossentropy', metrics=['accuracy'])
            model.fit(X_train, labels_train, batch_size=batch_s, epochs=epochs_s, callbacks = callback_list, class_weight=class_weight, verbose=2, validation_data=(X_test, labels_test))

            model.load_weights(weight_fn)
            prediction = model.predict(X_test);
            y_pred = np.argmax(prediction, axis=1)
    
            cr = classification_report(y_test, y_pred)
            cm = confusion_matrix(y_test, y_pred)
    
            print("-------------------- Full NN -----------------------")
            print("Skill: ", skill)
            print("Trial out:", user)
            acc = np.sum(y_pred == y_test)/y_pred.shape[0]
            acc_1.append(acc)
            print('Accuracy: ' + str(acc))
            print(cr)
            print(cm)
            f = open(str(tim)+'_'+skill+'_'+str(win)+'_'+str(over)+'_report_Resnet_fea.txt', 'a+')
            f.write("-------------------- Full NN -----------------------")
            f.write('---------' + skill + " Win: " + str(win) + " Shift: " + str(over) + " Trial: " + str(user) + '---------\n\n')
            f.write('Accuracy: ' + str(acc))
            f.write('\n\nClassification Report\n\n{}\n\nConfusion Matrix\n\n{}\n\n'.format(cr, cm))
            
            ##############################################
            moFea = Model(ip, fea)
            X_train_fea = moFea.predict(X_train)
            X_test_fea = moFea.predict(X_test)
            svm1 = svm.SVC(kernel = 'linear')
            svm1.fit(X_train_fea, y_train)
            prediction_fea = svm1.predict(X_test_fea)
            y_pred_fea = prediction_fea
            cr_fea = classification_report(y_test, y_pred_fea)
            cm_fea = confusion_matrix(y_test, y_pred_fea)
    
            acc_fea = np.sum(y_pred_fea == y_test)/y_pred_fea.shape[0]
            acc_1_fea.append(acc_fea)
            print('Accuracy: ' + str(acc_fea))
            print(cr_fea)
            print(cm_fea)
            f.write("-------------------- NN Fea -----------------------")
            f.write('---------' + skill + " Win: " + str(win) + " Shift: " + str(over) + " Trial: " + str(user) + '---------\n\n')
            f.write('Accuracy: ' + str(acc_fea))
            f.write('\n\nClassification Report\n\n{}\n\nConfusion Matrix\n\n{}\n\n'.format(cr_fea, cm_fea))
        for i in range(0,5):
            accu += acc_1[i]
            accu_fea += acc_1_fea[i]
        accu = accu/5
        accu_fea = accu_fea/5
        f.write("\n-------------------------------------------\n")
        f.write("Acc_full = " + str(accu))
        f.write("\nAcc_fea = " + str(accu_fea))
        f.write("\n-------------------------------------------\n")
        f.close()