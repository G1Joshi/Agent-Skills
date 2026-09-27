---
name: opencv
description: Expert OpenCV assistance covering computer vision, image filtering, edge detection, contour analysis, and real-time video processing. Use when processing visual data, building camera pipelines, or object detection.
---

# OpenCV

OpenCV is the fundamental library for Image Processing. v5.0 (2025) modernizes deep learning support and licensing.

## When to Use

- **Real-Time Computer Vision & Video Processing**: Frame-by-frame analysis of camera feeds, robotics, and industrial automation.
- **Image Preprocessing for Deep Learning**: Resizing, normalizing, thresholding, and color-space conversions.
- **Edge, Contour & Shape Detection**: Canny edge detection, Hough transforms, and bounding box polygon calculations.
- **Feature Matching & Homography**: Aligning perspectives and matching keypoints with ORB and SIFT.

## Quick Start

```python
import cv2

# Load image, convert to grayscale, apply Gaussian blur and Canny edge detection
img = cv2.imread("input.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
edges = cv2.Canny(blurred, threshold1=50, threshold2=150)

cv2.imwrite("edges.jpg", edges)
```

## Core Concepts

#Image Preprocessing, Thresholding & Contours

Detecting object shapes and drawing bounding boxes:

```python
import cv2
import numpy as np

# Load image in grayscale
image = cv2.imread('circuit_board.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Gaussian blur to reduce high-frequency noise
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Canny edge detection
edges = cv2.Canny(blurred, threshold1=50, threshold2=150)

# Find contours in the binary edge image
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

output = image.copy()
for cnt in contours:
    area = cv2.contourArea(cnt)
    if area > 100: # Filter small noise specks
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(output, f"Area: {int(area)}", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

cv2.imwrite('detected_components.jpg', output)
```

#Color Space Filtering with HSV Masking

Isolating colored objects independent of scene brightness:

```python
# Convert to Hue-Saturation-Value (HSV)
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Define range for blue color in HSV
lower_blue = np.array([100, 150, 50])
upper_blue = np.array([140, 255, 255])

# Threshold image to obtain binary mask
mask = cv2.inRange(hsv, lower_blue, upper_blue)

# Bitwise-AND mask and original image
blue_segmented = cv2.bitwise_and(image, image, mask=mask)
cv2.imwrite('blue_segmented.jpg', blue_segmented)
```

#Video Stream Processing Loop

Reading frames continuously from a camera feed or video file:

```python
cap = cv2.VideoCapture(0) # 0 = default webcam

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Process frame
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cv2.imshow('Live Monitor', gray_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

## Common Patterns

### Real-Time Video Stream Processing with FPS Throttling

**Problem**: Processing high-resolution webcam frames in Python causes frame buffering lag.

**Solution**:
Process frames in a tight loop with resolution resizing:

```python
cap = cv2.VideoCapture(0)
# Set capture resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break

    # Process frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('Live Stream', gray)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

## Best Practices (2026)

- **Do** remember OpenCV stores images in BGR format by default; convert with `cv2.COLOR_BGR2RGB` before Matplotlib/PyTorch.
- **Do** always release hardware resources (`cap.release()`) and destroy windows (`cv2.destroyAllWindows()`).
- **Do** use HSV or LAB color spaces rather than RGB when performing color-based segmentation under varying lighting.
- **Do** apply Gaussian or bilateral blurring prior to edge detection to suppress noise.
- **Don't** perform heavy deep learning inferences sequentially inside the video capture loop; use background threads.
- **Don't** hardcode kernel sizes with even numbers; blurring and morphological kernels should be odd (e.g. 3x3, 5x5).
- **Don't** assume `cv2.imread()` succeeded without checking if the returned array is not `None`.

## Troubleshooting

| Error                                                   | Cause                                                                   | Solution                                                         |
| :------------------------------------------------------ | :---------------------------------------------------------------------- | :--------------------------------------------------------------- |
| `cv2.error: (-215:Assertion failed) !ssize.empty()`     | `cv2.imread()` returned None because file path was wrong.               | Verify image file exists at specified path and is non-empty.     |
| `OpenCV: FFMPEG: tag 0x... is not supported with codec` | Incompatible video codec FourCC code during VideoWriter initialization. | Use `cv2.VideoWriter_fourcc(*'mp4v')` for MP4 video output.      |
| `Color distortion in exported image`                    | Displaying or saving BGR image as RGB (OpenCV default is BGR).          | Convert color space with `cv2.cvtColor(img, cv2.COLOR_BGR2RGB)`. |

## References

- [OpenCV Documentation](https://opencv.org/)
