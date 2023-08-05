import matplotlib.pyplot as plt

# TODO: refactor to check for image shape; if not the same reshape it
def plotRGBimages (titles, images, nrows=1, ncols=1, size=(8, 8), ticks=False,
                    channel_last=True, fontsize=12, cmap=plt.cm.gray):
    """
    Plot RGB images in a table format (nrows and ncols);
    
    # Arguments
        titles: list of titles to display on the top-centered of each images
            type: <class 'list'> of <class 'str'> 
            shape: (n, 1)
        images: list of images array
            type: <class 'numpy.ndarray'> of <class 'numpy.uint8'>
            shape: (n, x, y, channels)
        nrows: number of rows
        ncols: number of cols
        size: size of the figure or canvas, the table of images will be
            displayed on; may require manual trial-and-error to get is perfect
        tick: display the x and y axes tick marks
        channel_last: flag indicating the RGB image has channels last which is
            expected format for matpotlib.pyplot.imshow;
            When channel_last=False, the images is reshaped to channel last,
            assuming that the source images has channel first format, or
            (n, channels, x, y)
        fontsize: font size of the title
        cmap: matplotlib.pyplot.imshow colormap
            
    # Returns
        Figure
        
    # Raise
        None
    """
    # reshaping images to channel last
    if not channel_last:
        reshaped_images = images.reshape(images.shape[0], images.shape[2],
                                      images.shape[3], images.shape[1])

    fig = plt.figure(figsize=size)
    for i in range(nrows * ncols):
        if (i >= len(images)):
            break
        # label is needed for uniqueness of each plot
        plt.subplot(nrows, ncols, i + 1, label=i)
        plt.subplots_adjust(bottom=0, left=0, right=0.9, top=0.9, hspace=0.1,
                            wspace=0.05)
        plt.title(titles[i], size=fontsize)
        if not ticks:
            plt.xticks(())
            plt.yticks(())

        # need some logic for image src; avoid cloning for resource efficiency
        image = images[i] if channel_last else reshaped_images[i]

        plt.imshow(image, cmap=cmap)

