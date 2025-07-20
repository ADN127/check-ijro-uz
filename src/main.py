import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, render_template_string, abort, request, redirect, url_for, flash, jsonify, session
from werkzeug.utils import secure_filename
import re
import requests
from flask_cors import CORS

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# reCAPTCHA konfiguratsiyasi
RECAPTCHA_SECRET_KEY = '6LfmMokrAAAAAFSRsMuKi0vsptVhkJm3zjJECUK-'
RECAPTCHA_SITE_KEY = '6LfmMokrAAAAAFwjS5ZjBsBgwZcjTRlF-05g20FG'

# Enable CORS for all routes
CORS(app)

# PDF viewer route
@app.route('/d/<filename>')
def view_pdf(filename):
    # Check if PDF file exists
    pdf_path = os.path.join(app.static_folder, 'pdfs', f'{filename}.pdf')
    if not os.path.exists(pdf_path):
        not_found_template = '''
        <!DOCTYPE html>
        <html lang="uz">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Ижро интизоми</title>
            <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
            <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
            <script src="/static/captcha-overlay.js"></script>
            <style>
                * {
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }
                body {
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    background-color: #f8f9fa;
                    min-height: 100vh;
                }
                .header {
                    background-color: #ffffff;
                    border-bottom: 1px solid #e5e7eb;
                    padding: 8px 16px;
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    height: 64px;
                    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
                }
                .header-left {
                    display: flex;
                    align-items: center;
                    gap: 12px;
                }
                .menu-button {
                    background: none;
                    border: none;
                    cursor: pointer;
                    padding: 8px;
                    border-radius: 4px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: #6b7280;
                }
                .menu-button:hover {
                    background-color: #f3f4f6;
                }
                .logo-container {
                    display: flex;
                    align-items: center;
                    gap: 12px;
                }
                .logo {
                    width: 40px;
                    height: 40px;
                    border-radius: 50%;
                }
                .logo-text {
                    display: flex;
                    flex-direction: column;
                }
                .logo-title {
                    font-size: 16px;
                    font-weight: 600;
                    color: #1f2937;
                    line-height: 1.2;
                }
                .logo-subtitle {
                    font-size: 12px;
                    color: #6b7280;
                    line-height: 1.2;
                }
                .header-right {
                    display: flex;
                    align-items: center;
                }
                .search-container {
                    position: relative;
                    display: flex;
                    align-items: center;
                }
                .search-button {
                    background: none;
                    border: none;
                    cursor: pointer;
                    padding: 8px;
                    border-radius: 4px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: #6b7280;
                }
                .search-button:hover {
                    background-color: #f3f4f6;
                    color: #374151;
                }
                .search-overlay {
                    position: fixed;
                    top: 0;
                    left: 0;
                    right: 0;
                    background: white;
                    border-bottom: 1px solid #e5e7eb;
                    z-index: 1000;
                    height: 64px;
                    transform: translateY(-100%);
                    opacity: 0;
                    visibility: hidden;
                    transition: all 0.3s ease;
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                }
                .search-overlay.show {
                    transform: translateY(0);
                    opacity: 1;
                    visibility: visible;
                }
                .search-overlay-content {
                    width: 100%;
                    height: 64px;
                    display: flex;
                    align-items: center;
                    padding: 0 24px;
                }
                .search-form {
                    width: 100%;
                }
                .search-input-container {
                    position: relative;
                    width: 100%;
                    display: flex;
                    align-items: center;
                }
                .search-icon-left {
                    position: absolute;
                    left: 24px;
                    top: 50%;
                    transform: translateY(-50%);
                    color: #6b7280;
                    z-index: 1;
                }
                .search-overlay-input {
                    width: 100%;
                    padding-left: 64px;
                    padding-right: 64px;
                    height: 64px;
                    border: none;
                    outline: none;
                    font-size: 18px;
                    background: transparent;
                    color: #374151;
                }
                .search-overlay-input::placeholder {
                    color: #6b7280;
                }
                .search-overlay-close {
                    position: absolute;
                    right: 24px;
                    top: 50%;
                    transform: translateY(-50%);
                    background: none;
                    border: none;
                    cursor: pointer;
                    padding: 8px;
                    border-radius: 4px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: #6b7280;
                    transition: color 0.2s;
                }
                .search-overlay-close:hover {
                    color: #374151;
                }
                .not-found-container {
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    min-height: calc(100vh - 64px);
                    padding: 40px 20px;
                    text-align: center;
                }
                .not-found-icon {
                    width: 120px;
                    height: 120px;
                    margin-bottom: 24px;
                    color: #9ca3af;
                }
                .not-found-title {
                    font-size: 24px;
                    font-weight: 600;
                    color: #374151;
                    margin-bottom: 12px;
                }
                .not-found-message {
                    font-size: 16px;
                    color: #6b7280;
                    margin-bottom: 32px;
                    max-width: 400px;
                }
                .back-button {
                    background-color: #3b82f6;
                    color: white;
                    border: none;
                    padding: 12px 24px;
                    border-radius: 8px;
                    font-size: 16px;
                    font-weight: 500;
                    cursor: pointer;
                    transition: background-color 0.2s;
                    text-decoration: none;
                    display: inline-block;
                }
                .back-button:hover {
                    background-color: #2563eb;
                }
                @media (max-width: 768px) {
                    .logo-text {
                        display: none;
                    }
                    .header {
                        padding: 8px 12px;
                    }
                    .not-found-icon {
                        width: 80px;
                        height: 80px;
                    }
                    .not-found-title {
                        font-size: 20px;
                    }
                    .not-found-message {
                        font-size: 14px;
                    }
                }
            </style>
        </head>
        <body>
            <div class="header">
                <div class="header-left">
                    <button class="menu-button">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <line x1="3" y1="6" x2="21" y2="6"></line>
                            <line x1="3" y1="12" x2="21" y2="12"></line>
                            <line x1="3" y1="18" x2="21" y2="18"></line>
                        </svg>
                    </button>
                    <div class="logo-container">
                        <img src="/static/logo.png" alt="Logo" class="logo">
                        <div class="logo-text">
                            <div class="logo-title">Ижро интизоми</div>
                            <div class="logo-subtitle">Идоралараро ягона электрон тизими</div>
                        </div>
                    </div>
                </div>
                <div class="header-right">
                    <div class="search-container">
                        <button class="search-button" onclick="toggleSearchOverlay()">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <circle cx="11" cy="11" r="8"></circle>
                                <path d="m21 21-4.35-4.35"></path>
                            </svg>
                        </button>
                    </div>
                </div>
            </div>

            <!-- Search Overlay -->
            <div class="search-overlay" id="searchOverlay">
                <div class="search-overlay-content">
                    <form onsubmit="handleOverlaySearch(event)" class="search-form">
                        <div class="search-input-container">
                            <svg class="search-icon-left" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <circle cx="11" cy="11" r="8"></circle>
                                <path d="m21 21-4.35-4.35"></path>
                            </svg>
                            <input 
                                type="text" 
                                class="search-overlay-input" 
                                placeholder="Хужжат рақамини киритинг"
                                id="overlaySearchInput"
                                autocomplete="off"
                            >
                            <button type="button" class="search-overlay-close" onclick="closeSearchOverlay()">
                                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <line x1="18" y1="6" x2="6" y2="18"></line>
                                    <line x1="6" y1="6" x2="18" y2="18"></line>
                                </svg>
                            </button>
                        </div>
                    </form>
                </div>
            </div>

            <div class="not-found-container">
                <svg class="not-found-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                    <path d="M16 2v6h6"/>
                </svg>
                <h1 class="not-found-title">Ҳужжат топилмади</h1>
                <a href="/" class="back-button">Бош саҳифага қайтиш</a>
            </div>

            <script>
                let isSearchOpen = false;

                function toggleSearchOverlay() {
                    const overlay = document.getElementById('searchOverlay');
                    const overlayInput = document.getElementById('overlaySearchInput');
                    
                    isSearchOpen = !isSearchOpen;
                    
                    if (isSearchOpen) {
                        overlay.classList.add('show');
                        // Overlay ochilganda input ga fokus qo'yish
                        setTimeout(() => {
                            overlayInput.focus();
                        }, 100);
                    } else {
                        overlay.classList.remove('show');
                    }
                }

                function closeSearchOverlay() {
                    const overlay = document.getElementById('searchOverlay');
                    overlay.classList.remove('show');
                    isSearchOpen = false;
                }

                function handleOverlaySearch(event) {
                    event.preventDefault();
                    const searchInput = document.getElementById('overlaySearchInput');
                    const fileName = searchInput.value.trim();
                    
                    if (fileName) {
                        // PDF fayl nomini tozalash (faqat raqam va harflar)
                        const cleanFileName = fileName.replace(/[^a-zA-Z0-9]/g, '');
                        if (cleanFileName) {
                            window.location.href = `/d/${cleanFileName}`;
                        } else {
                            alert('Iltimos, to\\'g\\'ri fayl nomini kiriting');
                        }
                    } else {
                        alert('Iltimos, fayl nomini kiriting');
                    }
                }

                // Escape tugmasi bosilganda overlay ni yopish
                document.addEventListener('keydown', function(event) {
                    if (event.key === 'Escape' && isSearchOpen) {
                        closeSearchOverlay();
                    }
                });

                // Sahifa yuklanganda
                document.addEventListener('DOMContentLoaded', function() {
                    // Search overlay tashqarisiga bosilganda yopish
                    const overlay = document.getElementById('searchOverlay');
                    overlay.addEventListener('click', function(event) {
                        if (event.target === overlay) {
                            closeSearchOverlay();
                        }
                    });
                });
            </script>
        </body>
        </html>
        '''
        return render_template_string(not_found_template, filename=filename), 404
    
    # Return HTML page with PDF.js viewer
    html_template = '''
    <!DOCTYPE html>
    <html lang="uz">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{{ filename }} - Ижро интизоми</title>
        <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
        <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
        <script src="/static/captcha-overlay.js"></script>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background-color: #f8f9fa;
            }
            .header {
                background-color: #ffffff;
                border-bottom: 1px solid #e5e7eb;
                padding: 8px 16px;
                display: flex;
                align-items: center;
                justify-content: space-between;
                height: 64px;
                box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
            }
            .header-left {
                display: flex;
                align-items: center;
                gap: 12px;
            }
            .menu-button {
                background: none;
                border: none;
                cursor: pointer;
                padding: 8px;
                border-radius: 4px;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .menu-button:hover {
                background-color: #f3f4f6;
            }
            .logo-container {
                display: flex;
                align-items: center;
                gap: 12px;
            }
            .logo {
                width: 40px;
                height: 40px;
                border-radius: 50%;
            }
            .logo-text {
                display: flex;
                flex-direction: column;
            }
            .logo-title {
                font-size: 16px;
                font-weight: 600;
                color: #1f2937;
                line-height: 1.2;
            }
            .logo-subtitle {
                font-size: 12px;
                color: #6b7280;
                line-height: 1.2;
            }
            .header-right {
                display: flex;
                align-items: center;
            }
            .search-button {
                background: none;
                border: none;
                cursor: pointer;
                padding: 8px;
                border-radius: 4px;
                display: flex;
                align-items: center;
                justify-content: center;
                color: #6b7280;
            }
            .search-button:hover {
                background-color: #f3f4f6;
                color: #374151;
            }
            .pdf-container {
                width: 100%;
                height: calc(100vh - 64px);
                border: none;
            }
            .loading {
                text-align: center;
                padding: 50px;
                font-size: 18px;
                color: #666;
            }
            @media (max-width: 768px) {
                .logo-text {
                    display: none;
                }
                .header {
                    padding: 8px 12px;
                }
            }
        </style>
    </head>
    <body>
        <div class="header">
            <div class="header-left">
                <button class="menu-button">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <line x1="3" y1="6" x2="21" y2="6"></line>
                        <line x1="3" y1="12" x2="21" y2="12"></line>
                        <line x1="3" y1="18" x2="21" y2="18"></line>
                    </svg>
                </button>
                <div class="logo-container">
                    <img src="/static/logo.png" alt="Logo" class="logo">
                    <div class="logo-text">
                        <div class="logo-title">Ижро интизоми</div>
                        <div class="logo-subtitle">Идоралараро ягона электрон тизими</div>
                    </div>
                </div>
            </div>
            <div class="header-right">
                <button class="search-button">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <circle cx="11" cy="11" r="8"></circle>
                        <path d="m21 21-4.35-4.35"></path>
                    </svg>
                </button>
            </div>
        </div>
        <div class="loading" id="loading">PDF юкланмоқда...</div>
        <iframe 
            id="pdf-viewer"
            class="pdf-container" 
            src="/static/pdfjs/web/viewer.html?file=/static/pdfs/{{ filename }}.pdf"
            style="display: none;">
        </iframe>
        
        <script>
            document.getElementById('pdf-viewer').onload = function() {
                document.getElementById('loading').style.display = 'none';
                document.getElementById('pdf-viewer').style.display = 'block';
            };
        </script>
    </body>
    </html>
    '''
    return render_template_string(html_template, filename=filename)

# Serve PDF files
@app.route('/static/pdfs/<filename>')
def serve_pdf(filename):
    return send_from_directory(os.path.join(app.static_folder, 'pdfs'), filename)

# Admin page route
@app.route('/admin')
def admin_page():
    admin_template = '''
    <!DOCTYPE html>
    <html lang="uz">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Admin Panel - PDF Yuklash</title>
        <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
        <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
        <script src="/static/captcha-overlay.js"></script>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background-color: #f8f9fa;
                min-height: 100vh;
            }
            .header {
                background-color: #ffffff;
                border-bottom: 1px solid #e5e7eb;
                padding: 8px 16px;
                display: flex;
                align-items: center;
                justify-content: space-between;
                height: 64px;
                box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
            }
            .header-left {
                display: flex;
                align-items: center;
                gap: 12px;
            }
            .menu-button {
                background: none;
                border: none;
                cursor: pointer;
                padding: 8px;
                border-radius: 4px;
                display: flex;
                align-items: center;
                justify-content: center;
                color: #6b7280;
            }
            .menu-button:hover {
                background-color: #f3f4f6;
            }
            .logo-container {
                display: flex;
                align-items: center;
                gap: 12px;
            }
            .logo {
                width: 40px;
                height: 40px;
                border-radius: 50%;
            }
            .logo-text {
                display: flex;
                flex-direction: column;
            }
            .logo-title {
                font-size: 16px;
                font-weight: 600;
                color: #1f2937;
                line-height: 1.2;
            }
            .logo-subtitle {
                font-size: 12px;
                color: #6b7280;
                line-height: 1.2;
            }
            .admin-badge {
                background: #dc2626;
                color: white;
                padding: 4px 8px;
                border-radius: 12px;
                font-size: 12px;
                font-weight: 500;
            }
            .container {
                max-width: 600px;
                margin: 40px auto;
                padding: 0 20px;
            }
            .upload-card {
                background: white;
                border-radius: 12px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                padding: 30px;
            }
            .upload-title {
                font-size: 24px;
                font-weight: 700;
                color: #1f2937;
                margin-bottom: 8px;
                text-align: center;
            }
            .upload-subtitle {
                color: #6b7280;
                text-align: center;
                margin-bottom: 30px;
            }
            .form-group {
                margin-bottom: 20px;
            }
            .form-label {
                display: block;
                font-weight: 600;
                color: #374151;
                margin-bottom: 8px;
            }
            .form-input {
                width: 100%;
                padding: 12px 16px;
                border: 2px solid #e5e7eb;
                border-radius: 8px;
                font-size: 14px;
                transition: border-color 0.2s;
            }
            .form-input:focus {
                outline: none;
                border-color: #3b82f6;
            }
            .file-input-wrapper {
                position: relative;
                display: inline-block;
                width: 100%;
            }
            .file-input {
                position: absolute;
                opacity: 0;
                width: 100%;
                height: 100%;
                cursor: pointer;
            }
            .file-input-display {
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 40px 20px;
                border: 2px dashed #d1d5db;
                border-radius: 8px;
                background: #f9fafb;
                transition: all 0.2s;
                cursor: pointer;
            }
            .file-input-display:hover {
                border-color: #3b82f6;
                background: #eff6ff;
            }
            .file-input-display.has-file {
                border-color: #10b981;
                background: #ecfdf5;
            }
            .file-icon {
                margin-right: 12px;
                color: #6b7280;
            }
            .upload-btn {
                width: 100%;
                background: #3b82f6;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
                font-size: 16px;
                font-weight: 600;
                cursor: pointer;
                transition: background 0.2s;
            }
            .upload-btn:hover {
                background: #2563eb;
            }
            .upload-btn:disabled {
                background: #9ca3af;
                cursor: not-allowed;
            }
            .success-message {
                background: #dcfce7;
                border: 1px solid #bbf7d0;
                color: #166534;
                padding: 12px 16px;
                border-radius: 8px;
                margin-bottom: 20px;
                display: none;
            }
            .error-message {
                background: #fef2f2;
                border: 1px solid #fecaca;
                color: #dc2626;
                padding: 12px 16px;
                border-radius: 8px;
                margin-bottom: 20px;
                display: none;
            }
            .home-link {
                display: inline-flex;
                align-items: center;
                color: #3b82f6;
                text-decoration: none;
                font-weight: 500;
                margin-bottom: 20px;
            }
            .home-link:hover {
                color: #2563eb;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <div class="header-left">
                <button class="menu-button">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <line x1="3" y1="6" x2="21" y2="6"></line>
                        <line x1="3" y1="12" x2="21" y2="12"></line>
                        <line x1="3" y1="18" x2="21" y2="18"></line>
                    </svg>
                </button>
                <div class="logo-container">
                    <img src="/static/logo.png" alt="Logo" class="logo">
                    <div class="logo-text">
                        <div class="logo-title">Ижро интизоми</div>
                        <div class="logo-subtitle">Идоралараро ягона электрон тизими</div>
                    </div>
                </div>
            </div>
            <div class="admin-badge">ADMIN</div>
        </div>

        <div class="container">
            <a href="/" class="home-link">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="margin-right: 8px;">
                    <path d="m12 19-7-7 7-7"></path>
                    <path d="M19 12H5"></path>
                </svg>
                Bosh sahifaga qaytish
            </a>
            
            <div class="upload-card">
                <h1 class="upload-title">PDF Fayl Yuklash</h1>
                <p class="upload-subtitle">Yangi PDF hujjatni tizimga yuklang</p>
                
                <div id="successMessage" class="success-message"></div>
                <div id="errorMessage" class="error-message"></div>
                
                <form id="uploadForm" enctype="multipart/form-data">
                    <div class="form-group">
                        <label class="form-label">PDF Fayl</label>
                        <div class="file-input-wrapper">
                            <input type="file" id="pdfFile" name="pdf_file" accept=".pdf" class="file-input" required>
                            <div class="file-input-display" id="fileDisplay">
                                <svg class="file-icon" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                                    <polyline points="14,2 14,8 20,8"></polyline>
                                    <line x1="16" y1="13" x2="8" y2="13"></line>
                                    <line x1="16" y1="17" x2="8" y2="17"></line>
                                    <polyline points="10,9 9,9 8,9"></polyline>
                                </svg>
                                <span id="fileText">PDF faylni tanlash uchun bosing</span>
                            </div>
                        </div>
                    </div>
                    
                    <div class="form-group">
                        <label for="fileName" class="form-label">Fayl nomi (URL uchun)</label>
                        <input type="text" id="fileName" name="file_name" class="form-input" 
                               placeholder="Masalan: OJ2038108378" required 
                               pattern="[a-zA-Z0-9]+" title="Faqat ingliz harflari va raqamlar">
                    </div>
                    
                    <button type="submit" class="upload-btn" id="uploadBtn">
                        PDF Yuklash
                    </button>
                </form>
            </div>
        </div>

        <script>
            const fileInput = document.getElementById('pdfFile');
            const fileDisplay = document.getElementById('fileDisplay');
            const fileText = document.getElementById('fileText');
            const uploadForm = document.getElementById('uploadForm');
            const uploadBtn = document.getElementById('uploadBtn');
            const successMessage = document.getElementById('successMessage');
            const errorMessage = document.getElementById('errorMessage');

            fileInput.addEventListener('change', function(e) {
                const file = e.target.files[0];
                if (file) {
                    fileText.textContent = file.name;
                    fileDisplay.classList.add('has-file');
                } else {
                    fileText.textContent = 'PDF faylni tanlash uchun bosing';
                    fileDisplay.classList.remove('has-file');
                }
            });

            uploadForm.addEventListener('submit', async function(e) {
                e.preventDefault();
                
                const formData = new FormData();
                const file = fileInput.files[0];
                const fileName = document.getElementById('fileName').value.trim();
                
                if (!file) {
                    showError('Iltimos, PDF faylni tanlang');
                    return;
                }
                
                if (!fileName) {
                    showError('Iltimos, fayl nomini kiriting');
                    return;
                }
                
                if (!/^[a-zA-Z0-9]+$/.test(fileName)) {
                    showError('Fayl nomi faqat ingliz harflari va raqamlardan iborat bolishi kerak');
                    return;
                }
                
                formData.append('pdf_file', file);
                formData.append('file_name', fileName);
                
                uploadBtn.disabled = true;
                uploadBtn.textContent = 'Yuklanmoqda...';
                
                try {
                    const response = await fetch('/upload_pdf', {
                        method: 'POST',
                        body: formData
                    });
                    
                    const result = await response.json();
                    
                    if (response.ok) {
                        showSuccess(result.message + ' URL: /d/' + fileName);
                        uploadForm.reset();
                        fileText.textContent = 'PDF faylni tanlash uchun bosing';
                        fileDisplay.classList.remove('has-file');
                    } else {
                        showError(result.error || 'Yuklashda xatolik yuz berdi');
                    }
                } catch (error) {
                    showError('Yuklashda xatolik yuz berdi: ' + error.message);
                } finally {
                    uploadBtn.disabled = false;
                    uploadBtn.textContent = 'PDF Yuklash';
                }
            });
            
            function showSuccess(message) {
                successMessage.textContent = message;
                successMessage.style.display = 'block';
                errorMessage.style.display = 'none';
                setTimeout(() => {
                    successMessage.style.display = 'none';
                }, 5000);
            }
            
            function showError(message) {
                errorMessage.textContent = message;
                errorMessage.style.display = 'block';
                successMessage.style.display = 'none';
            }
        </script>
    </body>
    </html>
    '''
    return render_template_string(admin_template)

# PDF upload route
@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    # Captcha tekshiruvi
    if not session.get('captcha_verified', False):
        return jsonify({'error': 'Captcha tekshiruvi talab qilinadi'}), 403
    
    try:
        if 'pdf_file' not in request.files:
            return jsonify({'error': 'PDF fayl tanlanmagan'}), 400
        
        file = request.files['pdf_file']
        file_name = request.form.get('file_name', '').strip()
        
        if file.filename == '':
            return jsonify({'error': 'PDF fayl tanlanmagan'}), 400
        
        if not file_name:
            return jsonify({'error': 'Fayl nomi kiritilmagan'}), 400
        
        # Fayl nomini tekshirish
        if not re.match(r'^[a-zA-Z0-9]+$', file_name):
            return jsonify({'error': 'Fayl nomi faqat ingliz harflari va raqamlardan iborat bolishi kerak'}), 400
        
        # PDF fayl ekanligini tekshirish
        if not file.filename.lower().endswith('.pdf'):
            return jsonify({'error': 'Faqat PDF fayllar qabul qilinadi'}), 400
        
        # Fayl nomini xavfsiz qilish
        secure_name = secure_filename(f"{file_name}.pdf")
        
        # Faylni saqlash
        pdfs_dir = os.path.join(app.static_folder, 'pdfs')
        if not os.path.exists(pdfs_dir):
            os.makedirs(pdfs_dir)
        
        file_path = os.path.join(pdfs_dir, secure_name)
        file.save(file_path)
        
        return jsonify({
            'message': f'PDF fayl muvaffaqiyatli yuklandi: {file_name}.pdf',
            'file_name': file_name,
            'url': f'/d/{file_name}'
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Yuklashda xatolik: {str(e)}'}), 500

# Captcha sahifasi
@app.route('/captcha')
def captcha_page():
    return send_from_directory(app.static_folder, 'captcha.html')

# Captcha status tekshirish route
@app.route('/check_captcha_status', methods=['GET'])
def check_captcha_status():
    verified = session.get('captcha_verified', False)
    return jsonify({'verified': verified})

# Captcha tekshirish route
@app.route('/verify_captcha', methods=['POST'])
def verify_captcha():
    try:
        data = request.get_json()
        captcha_response = data.get('g-recaptcha-response')
        
        if not captcha_response:
            return jsonify({'success': False, 'error': 'Captcha javob topilmadi'}), 400
        
        # Google reCAPTCHA API ga so'rov yuborish
        verify_url = 'https://www.google.com/recaptcha/api/siteverify'
        verify_data = {
            'secret': RECAPTCHA_SECRET_KEY,
            'response': captcha_response,
            'remoteip': request.remote_addr
        }
        
        response = requests.post(verify_url, data=verify_data, timeout=10)
        result = response.json()
        
        if result.get('success', False):
            # Captcha muvaffaqiyatli tekshirildi
            session['captcha_verified'] = True
            session.permanent = True
            return jsonify({'success': True, 'message': 'Captcha muvaffaqiyatli tekshirildi'})
        else:
            error_codes = result.get('error-codes', [])
            error_message = 'Captcha tekshiruvida xatolik'
            if 'timeout-or-duplicate' in error_codes:
                error_message = 'Captcha muddati tugagan yoki takrorlangan'
            elif 'invalid-input-response' in error_codes:
                error_message = 'Noto\'g\'ri captcha javobi'
            
            return jsonify({'success': False, 'error': error_message}), 400
            
    except requests.RequestException as e:
        return jsonify({'success': False, 'error': 'Captcha xizmatiga ulanishda xatolik'}), 500
    except Exception as e:
        return jsonify({'success': False, 'error': f'Server xatoligi: {str(e)}'}), 500

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)

