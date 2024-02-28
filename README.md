# Hindsight Trader

Codebase for the Hindsight Trader app.

## Initial setup

```bash
make requirements
```

## Running locally

```bash
make run
```

## Running with Docker

```bash
# Create image
docker build -t hst-streamlit .

# Run the container
docker run -p 8501:8501 hst-streamlit
```

## Miscellaneous

- Logging config reference
  - [Code](https://github.com/mCodingLLC/VideosSampleCode/tree/master/videos/135_modern_logging)
  - [Video](https://www.youtube.com/watch?v=9L77QExPmI0)
