# QGAN for Fraud Dataset Generation ⚛️🤖

This project was developed during the **36-hour Quantum Conclave Hackathon conducted by SRM AP**, where our team won the **🏆 Best Industry Impact Award**.

The goal of this project is to address one of the biggest challenges in fraud detection: **imbalanced datasets**. Fraud cases are rare in real-world financial data, which makes it difficult for machine learning models to learn meaningful fraud patterns.

---

# 📌 Problem

Fraud detection datasets are highly imbalanced because fraudulent transactions occur very infrequently compared to legitimate ones.

Traditional oversampling techniques like **SMOTE**:
- assume relatively simple data distributions
- rely on linear interpolation
- often fail to capture complex relationships present in real fraud data

As a result, ML models trained on such data may struggle to generalize well.

---

# 💡 Proposed Solution

We propose using a **Quantum Generative Adversarial Network (QGAN)** to generate **high-quality synthetic fraud samples** that better capture complex data distributions.

QGAN combines:
- principles of **quantum computing**
- power of **Generative Adversarial Networks**
- probabilistic modelling capabilities

This allows generation of synthetic fraud data that:
- preserves complex relationships
- improves representation of minority class
- enhances model learning capability
- potentially increases fraud detection accuracy

---

# ⚙️ Tech Stack

- Python
- Quantum Machine Learning concepts
- Generative Adversarial Networks (GAN)
- Streamlit
- NumPy
- Pandas
- Scikit-learn
- Matplotlib

---

# 📂 Project Structure
qgan-fraud-detection/
│
├── qgan.py
│ Core implementation of Quantum GAN model
│
├── streamlit_qgan.py
│ Streamlit web app interface for generating synthetic fraud data
│
├── qgan_augmented_dataset.csv
│ Example generated dataset
│
├── requirements.txt
│ Required dependencies
│
└── README.md


---

# 🚀 How to Run the Project

### 1. Clone repository

### 2. Install dependencies

### 3. Run Streamlit app


The app will open in browser where synthetic fraud samples can be generated.

---

# 📊 Output

The QGAN model generates synthetic fraud samples that:
- increase representation of minority fraud class
- provide more complex patterns than traditional oversampling
- improve training dataset quality
- help machine learning models detect fraud more effectively

---

# 🔬 Why QGAN instead of SMOTE?

| Feature | SMOTE | QGAN |
|--------|------|------|
| Handles imbalance | Yes | Yes |
| Captures nonlinear patterns | Limited | Strong |
| Generates realistic data | Moderate | High |
| Uses quantum principles | No | Yes |
| Learns complex distributions | Limited | Better |

---

# 🏆 Achievement

**Best Industry Impact Award**  
Quantum Conclave Hackathon (36 hours)  
Conducted by SRM AP University

---

# 📈 Future Improvements

- Quantitative comparison with SMOTE and other augmentation techniques
- Hybrid classical-quantum GAN architecture
- Larger financial datasets
- API deployment
- Model performance benchmarking
- Research paper publication

---

# 👨‍💻 Author

Imthiyaaj Mynudeen

Masters in Data Science

---

# 📜 License

This project is open-source and available for academic and research purposes.
