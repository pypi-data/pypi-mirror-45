import matplotlib.pyplot as plt
import numpy as np

##############################################################################
# INFERENCE - assessment of Model performance
##############################################################################

def probability_histograms(titles, predictions, classmap, nrows=1, ncols=1,
                            size=(8, 8), xtick=True, ytick=False, fontsize=12):
    """
    Plot Probability Histogram of model predictions in a table format of 
    (nrows and ncols);
    
    # Arguments
        titles: list of titles to display on the top-centered of each images
            type: <class 'list'> of <class 'str'> 
            shape: (n, 1)
        images: list of images array
            type: <class 'numpy.ndarray'> of <class 'numpy.uint8'>
            shape: (n, x, y, channels)
        classmap: dictionary of class to label mapping
            type: <class 'dict'>
        nrows: number of rows
        ncols: number of cols
        size: size of the figure or canvas, the table of images will be
            displayed on; may require manual trial-and-error to get is perfect
        xtick, ytick: display the x and y axes tick marks
        fontsize: the fontsize of the title
            
    # Returns
        None
        
    # Raise
        None
    """
    n_classes = len(classmap)
    p_classes, p_labels, p_probs = predictions_topN(predictions, classmap,
                                                      topN=1)
    #size = (2.45 * ncols, 2.0 * nrows)
    fig = plt.figure(figsize=size)
    for i in range(nrows * ncols):
        if (i >= len(predictions)):
            break
        # label is needed for uniqueness of each plot
        plt.subplot(nrows, ncols, i + 1, label=i)
        plt.subplots_adjust(bottom=0, left=0, right=0.9, top=0.9, hspace=0.7,
                            wspace=0.05)
        probab = np.asscalar(p_probs[i])*100
        title = 'Actual: {}; \nPredict: {} ({:.1f}%)'.format(titles[i],
                      p_labels[i], probab)
        plt.title(title, size=fontsize)
        plt.xticks(range(n_classes))
        plt.xlim((-0.5, n_classes-0.5))
        plt.ylim((0,1))
        plt.bar(range(n_classes), predictions[i,:], align='center')
        if not xtick:
            plt.xticks(())
        if not ytick:
            plt.yticks(())
    return fig
    
    
def predictions_topN(predictions, classmap, topN=1):
    # get top N with prediction
    preds_class_topN = [np.argsort(pred)[::-1][:topN] for pred in predictions]
    preds_lbl_topN = [classmap[p[0]] for p in preds_class_topN]
    preds_prob_topN = [np.sort(pred)[::-1][:topN] for pred in predictions]
    preds_class_topN = np.array(preds_class_topN)
    preds_lbl_topN = np.array(preds_lbl_topN)
    preds_prob_topN = np.array(preds_prob_topN)
    
    return preds_class_topN, preds_lbl_topN, preds_prob_topN


def plotfeatures(features, figsize=(22,50), imgs_per_row=16):
    """
    Plot convolution features
    """
    # feature shape (n, m, #features), NOT for (1, w) for dense & flatten
    if len(features.shape) != 3:
        return
    n_features = features.shape[2]
    print("Number of features: ", n_features)
    ncols = imgs_per_row
    nrows = math.ceil(n_features / ncols)
    gridsize = (nrows, ncols)
    fig = plt.figure(figsize=figsize)
    ifeature = 0
    for irow in range(nrows):
        for icol in range(ncols):
            feature = features[:,:,ifeature]
            plt.subplot2grid(gridsize, (irow, icol))
            plt.subplots_adjust(bottom=0.01, left=0, right=0.9, top=0.11, hspace=0.1, wspace=0.25)
            title = "feat#{}".format(ifeature+1)
            plt.title(title)
            plt.imshow(feature, cmap="bone")
            plt.xticks(())
            plt.yticks(())
            ifeature += 1
            if ifeature == n_features:
                break


def activation_histogram(titles, activations, no_classes, nrows=1, ncols=1,
                          size=(35,6), xtick=True, ytick=True, fontsize=30):
    """
    Plot scalar activations on histograms
    """
    fig = plt.figure(figsize=size)
    for i in range(nrows * ncols):
        if (i >= len(activations)):
            break
        # label is needed for uniqueness of each plot
        plt.subplot(nrows, ncols, i + 1, label=i)
        plt.subplots_adjust(bottom=0, left=0, right=0.9, top=0.9, hspace=0.3,
                            wspace=0.05)
        plt.title(titles[i], size=fontsize)
        plt.xticks(range(no_classes[i]))
        plt.xlim((-0.5, no_classes[i]-0.5))
        plt.ylim((0,1))
        plt.bar(range(no_classes[i]), activations[i], align='center')
        if not xtick:
            plt.xticks(())
        if not ytick:
            plt.yticks(())


def activation_large_scalarvector(title, activation, figsize=(15,15),
                                    ticks=False):
    """
    Plot one scalar activation as a matrix plot.
    """
    # convert large scalar vector to square matrix
    square_size = int(np.floor(np.sqrt(activation.shape[0])))
    act_trunc = activation[0:square_size*square_size]
    act_matrix = act_trunc.reshape(square_size, square_size)
    fig = plt.figure(figsize=figsize)
    plt.title(title)
    plt.imshow(act_matrix, cmap="bone")
    if not ticks:
        plt.xticks(())
        plt.yticks(())