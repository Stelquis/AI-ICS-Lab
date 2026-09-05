import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.lines import Line2D
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def plot_loss_curve(loss_history, save_path, title='Training Loss Curve'):
    """绘制损失曲线，标注起点（绿）和终点（红）"""
    fig, ax = plt.subplots(figsize=(10, 6))
    epochs = range(1, len(loss_history) + 1)
    ax.plot(epochs, loss_history, 'b-', linewidth=2.5, marker='o', markersize=8)
    ax.scatter([1], [loss_history[0]], color='green', s=100, zorder=5,
                label=f'Start: {loss_history[0]:.4f}')
    ax.scatter([len(loss_history)], [loss_history[-1]], color='red', s=100, zorder=5,
                label=f'End:   {loss_history[-1]:.4f}')
    ax.set_xlabel('Epoch', fontsize=12)
    ax.set_ylabel('Loss', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend(fontsize=10)
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  损失曲线已保存: {save_path}")

def plot_decision_boundary_evolution(X, y, weights_history, save_path,
                                        title='Decision Boundary Evolution'):
    """将各 epoch 的决策边界叠加在同一图上，早期浅蓝、后期深蓝、最终黑色粗线。"""
    plt.figure(figsize=(12, 10))
    x_min, x_max = X[:, 0].min() - 0.5, X[:, 0].max() + 0.5
    y_min, y_max = X[:, 1].min() - 0.5, X[:, 1].max() + 0.5
    x_line = np.linspace(x_min, x_max, 200)
    plt.scatter(X[:, 0], X[:, 1], c=y,
                cmap=ListedColormap(['#FF4444', '#4444FF']),
                edgecolors='k', s=60, alpha=0.8, zorder=5)
    n = len(weights_history)
    for i, W in enumerate(weights_history):
        wd = W[:, 1] - W[:, 0]
        if abs(wd[2]) < 1e-6:
            continue
        y_line = -(wd[0] + wd[1] * x_line) / wd[2]
        mask = (y_line >= y_min) & (y_line <= y_max)
        if not mask.any():
            continue
        t = i / (n - 1) if n > 1 else 1.0  # 0 → 1 随 epoch 递增
        if i == n - 1:  # 最终边界：粗黑线
            plt.plot(x_line[mask], y_line[mask], 'k-', linewidth=3, zorder=4)
        else:  # 过渡边界：蓝色渐深
            plt.plot(x_line[mask], y_line[mask], '-',
                     color=(0, 0, 0.3 + 0.5 * t),
                     linewidth=1.0 + 2.0 * t,
                     alpha=0.2 + 0.7 * t,
                        zorder=3)
    legend = [
        Line2D([0], [0], color=(0, 0, 0.3), lw=1, alpha=0.4, label='Early Epochs'),
        Line2D([0], [0], color=(0, 0, 0.8), lw=2, alpha=0.9, label='Later Epochs'),
        Line2D([0], [0], color='black', lw=3, label=f'Final (Epoch {n})'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='#FF4444',
                markersize=10, linestyle='None', label='Class 0'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='#4444FF',
                markersize=10, linestyle='None', label='Class 1'),
    ]
    plt.legend(handles=legend, loc='upper right', fontsize=10)
    plt.xlabel('Feature 1', fontsize=12)
    plt.ylabel('Feature 2', fontsize=12)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  决策边界图已保存: {save_path}")

def visualize_training(X, y, loss_history, weights_history,
                        loss_filename='loss_curve.png',
                        boundary_filename='decision_boundary.png',
                        title_prefix=''):
    prefix = title_prefix.strip()
    plot_loss_curve(
        loss_history,
        save_path=os.path.join(SCRIPT_DIR, loss_filename),
        title=f'{prefix} Training Loss Curve'.strip()
    )
    plot_decision_boundary_evolution(
        X, y, weights_history,
        save_path=os.path.join(SCRIPT_DIR, boundary_filename),
        title=f'{prefix} Decision Boundary Evolution'.strip()
    )
