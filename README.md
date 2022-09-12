# Rippler

> A Python interface to the [Ripples drink printer platform](https://www.drinkripples.com). It reproduces the flow of the Ripples Web app, allowing for images to be sent to a machine programmatically.

## Features

* Get location of drink printers around a latitude/longitude
* Send an image (either a file, file-like object or public URL) to a machine's custom images queue

## Usage

```bash
pip install rippler
```

See [examples/](./examples) & [docs/](./docs)

## API flow

Typical API flow as used by the Web app.

```mermaid
sequenceDiagram
    participant Client
    participant API
    participant Image Upload Service
		
		%% Locations flow
		Note left of Client: Get Locations
		Client->>API: POST /locations
		API-->>Client: locations
		
		%% Upload image flow
		Note left of Client: Get Upload Image Service<br/>URL and parameters
		Client->>API: GET /getSignedUrl
		API-->>Client: upload service config
		
		Note left of Client: Upload Image
		Client->>Image Upload Service: POST /upload
		Image Upload Service-->>Client: uploaded image URL
		
		Note left of Client: Send Uploaded Image URL
		Client->>API: POST /pushUrl
		API-->>Client: Confirmation
```

