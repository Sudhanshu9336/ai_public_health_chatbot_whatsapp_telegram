from transformers import AutoTokenizer, TFAutoModel
import os

# Model name
model_name = "distilbert-base-uncased"

# Save path
save_path = r"D:\ai_public_health_chatbot_whatsapp_telegram\services\rasa\models\distilbert-base-uncased"

# Create folder if it doesn't exist
os.makedirs(save_path, exist_ok=True)

# Download tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = TFAutoModel.from_pretrained(model_name)

# Save locally
tokenizer.save_pretrained(save_path)
model.save_pretrained(save_path)

print("DistilBERT successfully downloaded and saved at:", save_path)
