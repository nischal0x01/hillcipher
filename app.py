"""
Hill Cipher Streamlit Application
This module provides a user-friendly interface for Hill Cipher encryption and decryption
with visual matrix operations and step-by-step explanations.
"""

import streamlit as st
import numpy as np
import pandas as pd
from cipher import HillCipher


def main():
    """
    Main Streamlit application for Hill Cipher.
    """
    st.set_page_config(page_title="Hill Cipher", page_icon="🔐", layout="wide")
    
    st.title("🔐 Hill Cipher Encryption & Decryption")
    st.markdown("---")
    
    # Initialize cipher
    cipher = HillCipher()
    
    # Sidebar for settings
    st.sidebar.header("Settings")
    
    # Key matrix size selection
    matrix_size = st.sidebar.selectbox("Key Matrix Size", [2, 3, 4], index=0)
    
    # Operation selection
    operation = st.sidebar.selectbox("Operation", ["Encrypt", "Decrypt"])
    
    # Auto-generate key matrix option
    if st.sidebar.button("🎲 Generate Random Key Matrix"):
        st.session_state.key_matrix = cipher.generate_random_key_matrix(matrix_size)
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📝 Input")
        
        # Text input
        if operation == "Encrypt":
            input_text = st.text_area("Enter Plaintext:", height=100, placeholder="Type your message here...")
        else:
            input_text = st.text_area("Enter Ciphertext:", height=100, placeholder="Type your encrypted message here...")
        
        st.subheader("🔑 Key Matrix")
        
        # Key matrix input - check if matrix size changed
        if ('key_matrix' not in st.session_state or 
            st.session_state.key_matrix.shape[0] != matrix_size):
            if matrix_size == 2:
                st.session_state.key_matrix = np.array([[3, 2], [5, 7]])
            elif matrix_size == 3:
                st.session_state.key_matrix = np.array([[6, 24, 1], [13, 16, 10], [20, 17, 15]])
            else:
                st.session_state.key_matrix = cipher.generate_random_key_matrix(matrix_size)
        
        # Display key matrix input fields
        key_matrix = np.zeros((matrix_size, matrix_size), dtype=int)
        
        st.write("Enter key matrix values:")
        for i in range(matrix_size):
            cols = st.columns(matrix_size)
            for j in range(matrix_size):
                with cols[j]:
                    key_matrix[i, j] = st.number_input(
                        f"[{i},{j}]", 
                        min_value=0, 
                        max_value=25, 
                        value=int(st.session_state.key_matrix[i, j]),
                        key=f"key_{i}_{j}"
                    )
        
        # Validate key matrix
        is_valid = cipher.is_valid_key_matrix(key_matrix)
        if is_valid:
            st.success("✅ Key matrix is valid (invertible mod 26)")
        else:
            st.error("❌ Key matrix is invalid (not invertible mod 26)")
        
        # Display key matrix
        st.write("**Key Matrix:**")
        st.write(key_matrix)
    
    with col2:
        st.header("📤 Output")
        
        if input_text and is_valid:
            try:
                if operation == "Encrypt":
                    result, steps = cipher.encrypt(input_text, key_matrix)
                    st.success(f"**Ciphertext:** {result}")
                else:
                    result, steps = cipher.decrypt(input_text, key_matrix)
                    st.success(f"**Plaintext:** {result}")
                
                # Store results for visualization
                st.session_state.last_result = result
                st.session_state.last_steps = steps
                st.session_state.last_operation = operation
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
        elif input_text and not is_valid:
            st.error("Please enter a valid key matrix first.")
        else:
            st.info("Enter text and a valid key matrix to see results.")
    
    # Character mapping display
    st.markdown("---")
    st.subheader("🔤 Character-Number Mapping")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        mapping = cipher.get_character_mapping()
        mapping_df = pd.DataFrame(
            [(char, num) for char, num in list(mapping.items())[:13]], 
            columns=['Character', 'Number']
        )
        st.dataframe(mapping_df, use_container_width=True)
    
    with col2:
        mapping_df2 = pd.DataFrame(
            [(char, num) for char, num in list(mapping.items())[13:]], 
            columns=['Character', 'Number']
        )
        st.dataframe(mapping_df2, use_container_width=True)
    
    # Visualization section
    if hasattr(st.session_state, 'last_steps') and st.session_state.last_steps:
        st.markdown("---")
        st.header("🔍 Step-by-Step Matrix Operations")
        
        steps = st.session_state.last_steps
        operation = st.session_state.last_operation
        
        # Create tabs for different views
        tab1, tab2, tab3 = st.tabs(["📊 Matrix Operations", "🔢 Numerical Steps", "📋 Summary"])
        
        with tab1:
            show_matrix_operations(steps, operation)
        
        with tab2:
            show_numerical_steps(steps, operation)
        
        with tab3:
            show_summary(steps, operation)


def show_matrix_operations(steps, operation):
    """
    Display matrix operations step by step.
    """
    st.subheader("Matrix Transformations")
    
    if operation == "Encrypt":
        st.write("**Encryption Process:**")
        st.write("For each block: Ciphertext = Key Matrix × Plaintext Block (mod 26)")
        
        # Show key matrix
        st.write("**Key Matrix:**")
        st.write(steps['key_matrix'])
        
        # Show each block operation
        for i, (plain_block, cipher_block) in enumerate(zip(steps['blocks'], steps['encrypted_blocks'])):
            st.write(f"**Block {i+1}:**")
            
            col1, col2, col3, col4, col5 = st.columns([2, 1, 2, 1, 2])
            
            with col1:
                st.write("Key Matrix")
                st.write(steps['key_matrix'])
            
            with col2:
                st.write("×")
            
            with col3:
                st.write("Plaintext Block")
                st.write(plain_block.reshape(-1, 1))
            
            with col4:
                st.write("=")
            
            with col5:
                st.write("Ciphertext Block")
                st.write(cipher_block.reshape(-1, 1))
    
    else:
        st.write("**Decryption Process:**")
        st.write("For each block: Plaintext = Key Matrix⁻¹ × Ciphertext Block (mod 26)")
        
        # Show key matrix and its inverse
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.write("**Key Matrix:**")
            st.write(steps['key_matrix'])
        
        with col2:
            st.write("**Inverse Key Matrix:**")
            st.write(steps['inverse_key_matrix'])
        
        # Show each block operation
        for i, (cipher_block, plain_block) in enumerate(zip(steps['blocks'], steps['decrypted_blocks'])):
            st.write(f"**Block {i+1}:**")
            
            col1, col2, col3, col4, col5 = st.columns([2, 1, 2, 1, 2])
            
            with col1:
                st.write("Inverse Key Matrix")
                st.write(steps['inverse_key_matrix'])
            
            with col2:
                st.write("×")
            
            with col3:
                st.write("Ciphertext Block")
                st.write(cipher_block.reshape(-1, 1))
            
            with col4:
                st.write("=")
            
            with col5:
                st.write("Plaintext Block")
                st.write(plain_block.reshape(-1, 1))


def show_numerical_steps(steps, operation):
    """
    Display numerical steps of the process.
    """
    st.subheader("Numerical Transformation Steps")
    
    if operation == "Encrypt":
        st.write("**1. Text Preprocessing:**")
        st.write(f"Original text: {steps['original_text']}")
        st.write(f"Padded text: {steps['padded_text']}")
        st.write(f"Numerical representation: {steps['text_numbers']}")
        
        st.write("**2. Block Processing:**")
        for i, (plain_block, cipher_block) in enumerate(zip(steps['blocks'], steps['encrypted_blocks'])):
            st.write(f"Block {i+1}: {plain_block} → {cipher_block}")
        
        st.write("**3. Final Result:**")
        st.write(f"Final numbers: {steps['final_numbers']}")
        st.write(f"Ciphertext: {steps['ciphertext']}")
    
    else:
        st.write("**1. Text Preprocessing:**")
        st.write(f"Ciphertext: {steps['ciphertext']}")
        st.write(f"Numerical representation: {steps['cipher_numbers']}")
        
        st.write("**2. Block Processing:**")
        for i, (cipher_block, plain_block) in enumerate(zip(steps['blocks'], steps['decrypted_blocks'])):
            st.write(f"Block {i+1}: {cipher_block} → {plain_block}")
        
        st.write("**3. Final Result:**")
        st.write(f"Final numbers: {steps['final_numbers']}")
        st.write(f"Plaintext: {steps['plaintext']}")


def show_summary(steps, operation):
    """
    Display a summary of the process.
    """
    st.subheader("Process Summary")
    
    if operation == "Encrypt":
        st.write("**Encryption Summary:**")
        st.info(f"✅ Successfully encrypted '{steps['original_text']}' to '{steps['ciphertext']}'")
        
        st.write("**Key Information:**")
        st.write(f"- Key matrix size: {steps['key_matrix'].shape[0]}×{steps['key_matrix'].shape[1]}")
        st.write(f"- Number of blocks processed: {len(steps['blocks'])}")
        st.write(f"- Text padding applied: {len(steps['padded_text']) - len(steps['original_text'])} characters")
    
    else:
        st.write("**Decryption Summary:**")
        st.info(f"✅ Successfully decrypted '{steps['ciphertext']}' to '{steps['plaintext']}'")
        
        st.write("**Key Information:**")
        st.write(f"- Key matrix size: {steps['key_matrix'].shape[0]}×{steps['key_matrix'].shape[1]}")
        st.write(f"- Number of blocks processed: {len(steps['blocks'])}")
        st.write(f"- Matrix inverse successfully computed")


if __name__ == "__main__":
    main()
