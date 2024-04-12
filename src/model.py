import torch

class Transformer_model: 
    def __init__(self, model):
        self.model = model.to("cuda" if torch.cuda.is_available() else "cpu") 
        self.device = self.model.device # Obtain the device from the model
        self.optimizer = torch.optim.AdamW(self.model.parameters(), lr=5e-5)

    def model_train(self, epochs, train_dataloader): 
        for epoch in range(epochs): # Use the specified number of epochs
            print("Epoch:", epoch)
            for idx, batch in enumerate(train_dataloader):
                input_ids = batch.pop("input_ids").to(self.device)
                pixel_values = batch.pop("pixel_values").to(self.device)

                outputs = self.model(input_ids=input_ids, pixel_values=pixel_values, labels=input_ids)

                loss = outputs.loss
                print("Loss:", loss.item())
                loss.backward()
                self.optimizer.step()
                self.optimizer.zero_grad()

        return self.model 

    @staticmethod
    def model_inference(image, processor, model): 
        inputs = processor(images=image, return_tensors="pt").to(model.device) 
        pixel_values = inputs.pixel_values
        generated_ids = model.generate(pixel_values=pixel_values)
        generated_caption = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
        print(generated_caption)

        
