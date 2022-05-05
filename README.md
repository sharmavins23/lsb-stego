# Least Significant Bit Steganography

[Steganography](https://en.wikipedia.org/wiki/Steganography) is the practice of
concealing a message within another message or physical object. Of course, the
point is on keeping encoded images relatively hidden, but outputting a garbage
image is kind of a red flag to most cryptographers.

The goal of this project is to take a working and (hopefully beautiful) photo
and encode a secondary photo in it without noticeably changing the image's
quality. The following is an image description of this:

![img](https://cdn.discordapp.com/attachments/883740406469234718/971184952131608676/unknown.png)

The leftmost color splotch is [#FF0000](https://color.aurlien.net/#FF0000). The
second color attempts to only change the least significant bit of the
_hexadecimal value_, which becomes [#FF0001](https://color.aurlien.net/#FF0001).
The third color changes the least significant bit of all digits, so the color
becomes [#FE0101](https://color.aurlien.net/#FE0101). With the third encoding
method, the encoded image size only has a limitation of being 1/8th (12.5%) of
the original image's size. This is the technique I will employ, and there's a
good diagram on how this encoding structure will work:

![img](https://hackaday.com/wp-content/uploads/2022/04/steganography-featured.jpg?w=800)

This image is featured in an article on
[Hackaday](https://hackaday.com/2022/05/01/how-to-hide-a-photo-in-a-photo/), the
concept of which I will attempt to create an encoding and decoding stream for.

## Current progress

Image encoding is done. However, for larger image sizes, this procedure is
ridiculously slow. Most of the holdup occurs on the binary conversion of each
pixel value (despite being linear time), so I've added a shortcut for skipping
this computation. It's recommended to only cloak smaller image files in large
images for runtime.

# License TL;DR

This project is distributed under the MIT license. This is a paraphrasing of a
[short summary](https://tldrlegal.com/license/mit-license).

This license is a short, permissive software license. Basically, you can do
whatever you want with this software, as long as you include the original
copyright and license notice in any copy of this software/source.

## What you CAN do:

-   You may commercially use this project in any way, and profit off it or the
    code included in any way;
-   You may modify or make changes to this project in any way;
-   You may distribute this project, the compiled code, or its source in any
    way;
-   You may incorporate this work into something that has a more restrictive
    license in any way;
-   And you may use the work for private use.

## What you CANNOT do:

-   You may not hold me (the author) liable for anything that happens to this
    code as well as anything that this code accomplishes. The work is provided
    as-is.

## What you MUST do:

-   You must include the copyright notice in all copies or substantial uses of
    the work;
-   You must include the license notice in all copies or substantial uses of the
    work.

If you're feeling generous, give credit to me somewhere in your projects.
