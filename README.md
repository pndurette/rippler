# Rippler

> A Python interface to the [Ripples drink printer platform](https://www.drinkripples.com). It reproduces the flow of the Ripples WebApp, allowing for images ("Ripples") to be sent programmatically to a Ripple Maker's mobile queue.

## Features

* Get location of Ripple Maker printers near a latitude/longitude
* Send an image (either a file, file-like object or public URL) to a printer's mobile images queue

## Usage

```bash
pip install rippler
```

See [examples/](./examples) & [docs/](./docs)

## About

This library is meant as a replacement for end-users who wish to create custom designs instead of using the Ripples WebApp. User-generated designs persist on a printer for 10 minutes.

## Image requirements

High contrast images with bold lines, 1700 x 1700 pixels, JPEG or PNG, Grayscale, 8 bit.

See [How to Make the Perfect Ripple](https://support.drinkripples.com/hc/en-us/articles/360018489672-How-to-Make-the-Perfect-Ripple).

## Disclaimer

This library is provided "as is" (see [LICENSE.md](LICENSE.md)) and is in no way associated with Ripples Ltd.