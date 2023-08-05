import matplotlib.pyplot as plt
import numpy as np

##############################################################################
# EVALUATION - Training results
##############################################################################

def plot_acc_loss(history, epochs, title=''):
    """
    Plot the "Accuracy" and "Loss" charts of the training 
    using the Keras "history" object returned by the training method 
    (fit, fit_generator, etc.)
    
    # Arguments
        history: object returned from the Keras training method
        epochs: number of epochs performed during the training;
            use to scale the x-axis (epoch)
        title: title of the plot; position at the top center
        
    # Returns
        The plot object (i.e., matplotlib.pyplot)
    
    # Raise
        None
    """
    f, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    t = f.suptitle(title, fontsize=12)
    f.subplots_adjust(top=0.85, wspace=0.3)

    epoch_list = list(range(0, epochs))
    ax1.plot(epoch_list, history.history['acc'], label='Train Accuracy')
    ax1.plot(epoch_list, history.history['val_acc'], 
              label='Validation Accuracy')
    ax1.set_xticks(np.arange(0, epochs, epochs/10))
    ax1.set_ylabel('Accuracy Value')
    ax1.set_xlabel('Epoch')
    ax1.set_title('Accuracy')
    l1 = ax1.legend(loc="best")

    ax2.plot(epoch_list, history.history['loss'], label='Train Loss')
    ax2.plot(epoch_list, history.history['val_loss'], 
              label='Validation Loss')
    ax2.set_xticks(np.arange(0, epochs, epochs/10))
    ax2.set_ylabel('Loss Value')
    ax2.set_xlabel('Epoch')
    ax2.set_title('Loss')
    l2 = ax2.legend(loc="best")
    
    return plt