# Critical Thinking Module 2

**Program:** [Module2_CTA.py](Module2_CTA.py) - Color channel extraction, reconstruction, and red/green swapping

**Date:** 09/27/2026  
**Grade:**

---

Foundations of Computer Vision CSC515   
Professor: Dr. Binbong Li 
Fall C (26FC) – 2026   
Student: Alexander (Alex) Ricciardi  

---


## Assignment:

After completing the Required Reading, you should have a good idea of how to use OpenCV for multi-scale representation of images by pixels matrices. Select and take a look at one of the following images:

image of a [puppy](org_images/puppy.jpg)
image of a [kitten](org_images/kitty.jpg)

As both are colored images, each image has three channels, corresponding to the primary colors of red, green, and blue.

Import your selected image (using the link) into OpenCV and write code to extract each of these channels separately to create 2D images. This means that from the n x n x 3 shaped image, you will get 3 matrices of the shape n x n.
Now, write code to merge all these images back into a colored 3D image.
What will the image look like if you exchange the reds with the greens? Write code to merge the 2D images created in step 1 back together, this time swapping out the red channel with the green channel (GRB).
Be sure to display the resulting images for each step. Your submission should be one executable Python file.


---

## Program Requirements

[![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![OpenCV 4.13.0](https://img.shields.io/badge/OpenCV-4.13.0-5C3EE8?style=flat&logo=opencv&logoColor=white)](https://opencv.org/)
[![NumPy 2.5.3](https://img.shields.io/badge/NumPy-2.5.3-013243?style=flat&logo=numpy&logoColor=white)](https://numpy.org/)

[![iTerm2](https://img.shields.io/badge/iTerm2-Inline%20Images-000000?style=flat&logo=iterm2&logoColor=white)](https://iterm2.com/)

iTerm2 capable terminal is required to display images in terminal. 
The program uses Term-Image's `ITerm2Image` to display PNG graphics at
the terminal's pixel resolution. 

### Images in terminal

On Mac OS, Antigravity IDE's terminal is recommended to view the PNG image correctly.  
[iTerm2](https://iterm2.com/documentation-images.html) is another option as it supports displaying PNG images directly inside the terminal. 

---

## The Program

The program uses the [puppy image](org_images/puppy.jpg) to perform color transformation using OPenCV
The program separates Blue, Green, and Red (BGR) color values of the image and creates
another image by swapping the red and green values. 
- Blue → stays Blue
- Green → moves into the Red position
- Red → moves into the Green position

<img width="771" height="203" alt="image" src="https://github.com/user-attachments/assets/e15e3124-ba6c-4185-b440-ca8834a80d8c" />

### How to run the program

```bash
python -m pip install -r requirements.txt
python Module2_CTA.py
```

### Image structure

OpenCV decodes the puppy JPEG into a `uint8` array with shape `(257, 250, 3)`.
That means 257 rows, 250 columns, and three color values at each pixel. Here,
`uint8` means that each value is an unsigned 8-bit integer, from 0 to 255.


### Extracting the channels

```python
blue, green, red = cv2.split(image)
```

This one call returns three separate 2D arrays. Each has shape `(257, 250)` and
keeps the original values for one channel. For example, `red[row, column]` is the
red value from that same position in the original image.

The saved channel images appear in grayscale. A bright pixel in the red-channel
image means that the original pixel has a high red value; a dark pixel means it
has a low red value. Black represents 0, and white represents 255. This is not a
weighted grayscale conversion of the whole color image. It displays the values
of one channel.

The selection can be represented with a matrix. For red, a 1 selects the third
component of the BGR pixel, while the two 0s ignore blue and green:

```text
                 [ B ]
R = [0  0  1]  @ [ G ]
                 [ R ]

R = 0*B + 0*G + 1*R
```

Blue uses `[1 0 0]`, and green uses `[0 1 0]`. The `@` symbol means matrix
multiplication. These matrices describe what the channel operations do; the
script uses `cv2.split()` and `cv2.merge()` instead of explicitly multiplying
each pixel's color values by these matrices.

### Reconstructing the original image

```python
reconstructed = cv2.merge((blue, green, red))
```

This puts the three 2D arrays back into their original BGR positions. At each
pixel, blue goes into the blue position, green into green, and red into red.
The result has shape `(257, 250, 3)` and the same pixel values as the decoded
original image.

Splitting and then merging in this order is equivalent to applying the identity
matrix, which leaves the values unchanged. The prime mark (`'`) below identifies
an output value.

```text
[B']   [1  0  0]   [B]   [B]
[G'] = [0  1  0] @ [G] = [G]
[R']   [0  0  1]   [R]   [R]
```

### Swapping red and green

```python
swapped = cv2.merge((blue, red, green))
```

For the second merge, I keep blue in its original position and exchange the
other two channels. The original red values go into the output's green position,
and the original green values go into its red position. The matrix shows that
exchange:

```text
[B']   [1  0  0]   [B]   [B]
[G'] = [0  0  1] @ [G] = [R]
[R']   [0  1  0]   [R]   [G]
```

This is a permutation matrix: it rearranges the components rather than changing
their individual intensity values. For example, an original BGR pixel
`[20, 100, 200]` becomes `[20, 200, 100]`. Its blue value stays at 20, its new
green value is 200, and its new red value is 100. Its row and column do not change.

The output still uses BGR storage. Its values come from the original channels in
the order `(blue, red, green)`. When described in RGB order, those same output
colors are `(original green, original red, original blue)`, or GRB, as requested
in the assignment.

### Reading the terminal comparisons

I added the matrix explanations above the pictures so we can connect each code
operation to its result. Before each comparison, the script prints the relevant
code, the matrix, and a numerical example using the center pixel of the loaded
image. It also shows the input and output array shapes. The example values printed
in the terminal come from the image, rather than the illustrative values used
above.

The comparison panels are arranged as follows when the terminal is wide enough:

```text
Channel extraction:
Original | Selected channel in its own color | 2D grayscale result

Reconstruction:
Original | Blue -> B slot | Green -> G slot | Red -> R slot | Result

Red/green swap:
Original | Blue -> B slot | Red -> G slot | Green -> R slot | Result
```

For channel extraction, the middle panel is only a visual aid. It shows the
selected channel in its own color by setting the other two channels to zero in
a separate preview array. The grayscale panel is the actual 2D result from
`cv2.split()`; it is not produced by converting that colored preview to grayscale.

For the two merge operations, the middle panels show the actual 2D input arrays.
Their labels identify the output channel that receives each array. For example,
`Red -> G slot` means that the original red values become the output's green
values. All five results use channels from the same original image; one displayed
result is not used as the source for the next transformation.

The program saves all five results before displaying the comparisons. The previews
use the image arrays in memory and are resized to fit the terminal. PNG rendering
preserves the full color range instead of reducing it to a 256-color palette.
Preview resizing does not affect the saved PNGs, and the extra visual-aid panels
are not saved as additional results.

### Saved files

| Output | Contents |
| --- | --- |
| [red_channel.png](mod_images/red_channel.png) | Original red values; 2D `uint8`, 257 × 250. |
| [green_channel.png](mod_images/green_channel.png) | Original green values; 2D `uint8`, 257 × 250. |
| [blue_channel.png](mod_images/blue_channel.png) | Original blue values; 2D `uint8`, 257 × 250. |
| [reconstructed.png](mod_images/reconstructed.png) | Original decoded colors; `uint8`, 257 × 250 × 3. |
| [red_green_swapped.png](mod_images/red_green_swapped.png) | Red and green exchanged, blue unchanged; `uint8`, 257 × 250 × 3. |

The original puppy and kitten JPEGs are preserved. The kitten is an unused
alternative supplied with the assignment; no additional image source or license
is asserted.

---

## Files map

```text
CTA_Module-2/
├── README.md                                        # Program documentation
├── Module2_CTA.py                                   # Single executable image-processing program
├── CTA2– Program Explanation and Screenshots.pdf    # Contains The program explanation and screenshots 
├── org_images/                                      # Contains the orginal image
│   ├── puppy.jpg                                    # Selected original input
│   └── kitty.jpg                                    # Preserved alternative input
├── mod_images/                                      # Contains the modified images
│   ├── red_channel.png
│   ├── green_channel.png
│   ├── blue_channel.png
│   ├── reconstructed.png
│   └── red_green_swapped.png
```


---

My Links:

<p align="left">
<a href="https://github.com/AngryOwlAI/"><img width="25" height="25" src="https://github.com/user-attachments/assets/ef169f03-2a25-4737-95e8-9b6a85491c9c" alt="AngryOwlAI logo"><img height="30" src="https://img.shields.io/badge/AngryOwlAI-0D1117?style=for-the-badge" alt="AngryOwlAI GitHub organization"></a>
<a href="https://www.alexomegapy.com"><img width="27" height="27" src="https://github.com/user-attachments/assets/a8e0ea66-5d8f-43b3-8fff-2c3d74d57f53" alt="Code Chronicles logo"></a><a href="https://www.alexomegapy.com"><img height="30" src="https://img.shields.io/badge/Code%20Chronicles%20%7C%20Omegapy-0D1117?style=for-the-badge" alt="Code Chronicles | Omegapy"></a>
<a href="https://medium.com/@alex.omegapy"><img height="30" src="https://img.shields.io/badge/Medium-12100E?style=for-the-badge&logo=medium&logoColor=white" alt="Medium"></a>
<a href="https://x.com/AlexOmegapy"><img height="30" src="https://img.shields.io/badge/X-000000?style=for-the-badge&logo=x&logoColor=white" alt="X"></a>
<a href="https://www.youtube.com/@AngryOwl-AI"><img height="30" src="https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white" alt="YouTube"></a>
<a href="https://www.facebook.com/profile.php?id=100089638857137"><img height="30" src="https://img.shields.io/badge/Facebook-1877F2?style=for-the-badge&logo=facebook&logoColor=white" alt="Facebook"></a>
<a href="https://linkedin.com/in/alex-ricciardi"><img height="30" src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"></a>
<a href="https://www.threads.net/@alexomegapy?hl=en"><img height="30" src="https://img.shields.io/badge/Threads-000000?style=for-the-badge&logo=threads&logoColor=white" alt="Threads"></a>
<a href="https://dev.to/alex_ricciardi"><img height="30" src="https://img.shields.io/badge/DEV.to-0A0A0A?style=for-the-badge&logo=devdotto&logoColor=white" alt="DEV.to"></a>
</p>
 
