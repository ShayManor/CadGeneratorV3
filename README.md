# Cadalix

AI-powered CAD model generation platform that creates 3D models from natural language descriptions.

## API Endpoints

### Create Model
```http
POST https://cadalix-675492064948.us-central1.run.app/create_model
Content-Type: application/json

{
    "prompt": "A simple coffee mug with a handle",
    "model_name": "Mug"
}
```

### List Models
```http
GET https://cadalix-675492064948.us-central1.run.app/list_models
```

### Get Model
```http
POST https://cadalix-675492064948.us-central1.run.app/get_model
Content-Type: application/json

{
    "name": "Mug"
}
```

## Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`.

## Features

- Generate 3D models from text descriptions
- Interactive 3D model viewer
- Real-time model preview
- Export models in standard formats