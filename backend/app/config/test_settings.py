from app.config import settings

# Override settings for testing environment
settings.ENVIRONMENT = "test"

# Add mock model settings for tests that don't need a real model
settings.MOCK_MODEL_IN_TESTS = True
