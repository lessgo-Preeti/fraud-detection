"""
Neural Network Model Architecture for Fraud Detection
Implements MLP with regularization techniques
"""

import tensorflow as tf
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config


class FraudDetectionModel:
    """
    Multilayer Perceptron for Credit Card Fraud Detection
    """
    
    def __init__(self):
        self.config = Config()
        self.model = None
        self.history = None
        
    def build_model(self):
        """
        Build the neural network architecture
        
        Architecture:
        - Input Layer: 30 features
        - Hidden Layer 1: 64 neurons, ReLU, L2 regularization, Dropout
        - Hidden Layer 2: 32 neurons, ReLU, L2 regularization, Dropout
        - Output Layer: 1 neuron, Sigmoid
        
        Returns:
            keras.Model: Compiled model
        """
        print("\nBuilding Neural Network Model...")
        print("="*50)
        
        model = tf.keras.Sequential([
            # Input layer
            tf.keras.layers.Dense(
                self.config.HIDDEN_LAYERS[0],
                input_dim=self.config.INPUT_DIM,
                activation='relu',
                kernel_regularizer=tf.keras.regularizers.l2(self.config.L2_REGULARIZATION),
                name='hidden_layer_1'
            ),
            tf.keras.layers.Dropout(self.config.DROPOUT_RATE, name='dropout_1'),
            
            # Hidden layer 2
            tf.keras.layers.Dense(
                self.config.HIDDEN_LAYERS[1],
                activation='relu',
                kernel_regularizer=tf.keras.regularizers.l2(self.config.L2_REGULARIZATION),
                name='hidden_layer_2'
            ),
            tf.keras.layers.Dropout(self.config.DROPOUT_RATE, name='dropout_2'),
            
            # Output layer
            tf.keras.layers.Dense(1, activation='sigmoid', name='output_layer')
        ])
        
        # Compile the model
        model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=self.config.LEARNING_RATE),
            loss='binary_crossentropy',
            metrics=[
                'accuracy',
                tf.keras.metrics.Precision(name='precision'),
                tf.keras.metrics.Recall(name='recall'),
                tf.keras.metrics.AUC(name='auc')
            ]
        )
        
        self.model = model
        
        print("\nModel Architecture:")
        self.model.summary()
        
        return model
    
    def get_callbacks(self):
        """
        Define training callbacks
        
        Returns:
            list: List of callbacks
        """
        callbacks = [
            # Early stopping to prevent overfitting
            tf.keras.callbacks.EarlyStopping(
                monitor='val_loss',
                patience=self.config.EARLY_STOPPING_PATIENCE,
                restore_best_weights=True,
                verbose=1
            ),
            
            # Save best model
            tf.keras.callbacks.ModelCheckpoint(
                self.config.MODEL_SAVE_PATH,
                monitor='val_auc',
                save_best_only=True,
                mode='max',
                verbose=1
            ),
            
            # Reduce learning rate on plateau
            tf.keras.callbacks.ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=5,
                min_lr=1e-7,
                verbose=1
            )
        ]
        
        return callbacks
    
    def train(self, X_train, y_train, X_val=None, y_val=None):
        """
        Train the model
        
        Args:
            X_train: Training features
            y_train: Training labels
            X_val: Validation features (optional)
            y_val: Validation labels (optional)
            
        Returns:
            History: Training history
        """
        if self.model is None:
            self.build_model()
        
        print("\n" + "="*50)
        print("TRAINING MODEL")
        print("="*50)
        
        # Calculate class weights for imbalanced data
        total = len(y_train)
        neg_count = (y_train == 0).sum()
        pos_count = (y_train == 1).sum()
        
        weight_for_0 = (1 / neg_count) * (total / 2.0)
        weight_for_1 = (1 / pos_count) * (total / 2.0)
        
        class_weight = {0: weight_for_0, 1: weight_for_1}
        
        print(f"\nClass weights: {class_weight}")
        
        # Prepare validation data
        validation_data = None
        if X_val is not None and y_val is not None:
            validation_data = (X_val, y_val)
        else:
            validation_data = None
            print("No validation data provided, using validation_split from config")
        
        # Train the model
        self.history = self.model.fit(
            X_train, y_train,
            epochs=self.config.EPOCHS,
            batch_size=self.config.BATCH_SIZE,
            validation_split=self.config.VALIDATION_SPLIT if validation_data is None else 0.0,
            validation_data=validation_data,
            class_weight=class_weight,
            callbacks=self.get_callbacks(),
            verbose=1
        )
        
        print("\n" + "="*50)
        print("TRAINING COMPLETED!")
        print("="*50)
        
        return self.history
    
    def load_model(self, model_path=None):
        """
        Load a saved model
        
        Args:
            model_path (str): Path to saved model
            
        Returns:
            Model if successful, None if file not found
        """
        if model_path is None:
            model_path = self.config.MODEL_SAVE_PATH
        
        # Check if file exists before trying to load
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at {model_path}")
        
        print(f"Loading model from {model_path}...")
        self.model = tf.keras.models.load_model(model_path)
        print("Model loaded successfully!")
        
        return self.model
    
    def predict(self, X, threshold=0.5):
        """
        Make predictions
        
        Args:
            X: Input features
            threshold (float): Classification threshold
            
        Returns:
            tuple: (probabilities, predictions)
        """
        probabilities = self.model.predict(X)
        predictions = (probabilities > threshold).astype(int)
        
        return probabilities, predictions


if __name__ == "__main__":
    # Test model building
    fraud_model = FraudDetectionModel()
    model = fraud_model.build_model()
    print("\nModel built successfully!")
