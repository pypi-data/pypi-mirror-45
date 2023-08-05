import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

# either functional / factory
# or object-oriented can be better

def loss_plot():
    if max_epoch is not None:
        plt.xlim(1, max_epoch)

    for i, (serie_label, serie_fmt) in enumerate(series_fmt.items()):

        if serie_fmt.format(metric) in logs[0]:
            serie_metric_name = serie_fmt.format(metric)
            serie_metric_logs = [log[serie_metric_name] for log in logs]
            plt.plot(range(1, len(logs) + 1),
                        serie_metric_logs,
                        label=serie_label)

    plt.title(metric2title.get(metric, metric))
    plt.xlabel('epoch')
    plt.legend(loc='center right')

# we need some idea to make a general way of passing:
# model
# model predictions
# other data (e.g. train and test data points)
def predict_pytorch(model, x_numpy):
    import torch
    x = torch.from_numpy(x_numpy).float()
    return model(x).softmax(dim=1).detach().numpy()

def draw_prediction_map(model, with_points=True):
    cm = plt.cm.RdBu
    cm_bright = ListedColormap(['#FF0000', '#0000FF'])

    h = .02  # step size in the mesh
    x_min = X[:, 0].min() - .5
    x_max = X[:, 0].max() + .5

    y_min = X[:, 1].min() - .5
    y_max = X[:, 1].min() - .5

    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                     np.arange(y_min, y_max, h))

    # class 1 is true
    Z = predict_pytorch(model, np.c_[xx.ravel(), yy.ravel()])[:, 1]
    Z = Z.reshape(xx.shape)
    plt.contourf(xx, yy, Z, cmap=cm, alpha=.8)
    if with_points:
        plt.scatter(X_train[:, 0], X_train[:, 1], c=y_train, cmap=cm_bright)
        plt.scatter(X_test[:, 0], X_test[:, 1], c=y_test, cmap=cm_bright, alpha=0.3)


# 1d

plt.plot(X.squeeze(1).numpy(), Y.numpy(), 'r.')
plt.plot(X.squeeze(1).numpy(), linear_model(X).detach().numpy(), '-')

# example predicitons
