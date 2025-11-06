#!/usr/bin/env python3
"""
Modern Theme Configuration
Provides consistent dark and light theme styling for tkinter applications
"""

import tkinter as tk
from tkinter import ttk


class ModernTheme:
    """Modern theme configuration for the application"""
    
    # Color palette - Modern dark theme
    DARK_BG = "#2b2b2b"
    DARKER_BG = "#1e1e1e"
    CARD_BG = "#3c3c3c"
    ACCENT = "#007acc"
    ACCENT_HOVER = "#005a9e"
    SUCCESS = "#4caf50"
    WARNING = "#ff9800"
    ERROR = "#f44336"
    TEXT_PRIMARY = "#ffffff"
    TEXT_SECONDARY = "#b0b0b0"
    BORDER = "#555555"
    
    # Light theme alternative
    LIGHT_BG = "#ffffff"
    LIGHT_CARD_BG = "#f8f9fa"
    LIGHT_TEXT_PRIMARY = "#212529"
    LIGHT_TEXT_SECONDARY = "#6c757d"
    LIGHT_BORDER = "#dee2e6"
    
    @classmethod
    def configure_modern_style(cls, root, theme="dark"):
        """Configure modern ttk styles"""
        style = ttk.Style(root)
        
        if theme == "dark":
            cls._configure_dark_theme(style, root)
        else:  # light theme
            cls._configure_light_theme(style, root)
        
        # Configure light device dropdown (always light regardless of theme)
        cls._configure_light_device_dropdown(style)
        
        return style
    
    @classmethod
    def _configure_dark_theme(cls, style, root):
        """Configure dark theme styles"""
        style.theme_use('clam')
        
        # Configure base colors
        style.configure(".", 
                      background=cls.DARK_BG,
                      foreground=cls.TEXT_PRIMARY,
                      bordercolor=cls.BORDER,
                      fieldbackground=cls.CARD_BG,
                      selectbackground=cls.ACCENT,
                      selectforeground=cls.TEXT_PRIMARY,
                      insertcolor=cls.TEXT_PRIMARY)
        
        # Configure widgets
        cls._configure_buttons(style, cls.ACCENT, cls.ACCENT_HOVER)
        cls._configure_entry_combobox(style, cls.CARD_BG, cls.BORDER, cls.TEXT_SECONDARY)
        cls._configure_labels(style, cls.DARK_BG, cls.TEXT_PRIMARY, cls.TEXT_SECONDARY)
        cls._configure_checkbutton(style, cls.DARK_BG, cls.TEXT_PRIMARY)
        cls._configure_status_labels(style, cls.DARK_BG)
        
        # Configure root window
        root.configure(bg=cls.DARK_BG)
    
    @classmethod
    def _configure_light_theme(cls, style, root):
        """Configure light theme styles"""
        style.theme_use('clam')
        
        # Configure base colors
        style.configure(".", 
                      background=cls.LIGHT_BG,
                      foreground=cls.LIGHT_TEXT_PRIMARY,
                      bordercolor=cls.LIGHT_BORDER,
                      fieldbackground=cls.LIGHT_CARD_BG,
                      selectbackground=cls.ACCENT,
                      selectforeground=cls.TEXT_PRIMARY,
                      insertcolor=cls.LIGHT_TEXT_PRIMARY)
        
        # Configure widgets
        cls._configure_buttons(style, cls.ACCENT, cls.ACCENT_HOVER)
        cls._configure_entry_combobox(style, cls.LIGHT_CARD_BG, cls.LIGHT_BORDER, cls.LIGHT_TEXT_SECONDARY)
        cls._configure_checkbutton(style, cls.LIGHT_BG, cls.LIGHT_TEXT_PRIMARY)
        
        # Configure root window
        root.configure(bg=cls.LIGHT_BG)
    
    @classmethod
    def _configure_buttons(cls, style, bg_color, hover_color):
        """Configure button styles"""
        # Modern button style
        style.configure("Modern.TButton",
                      background=bg_color,
                      foreground=cls.TEXT_PRIMARY,
                      borderwidth=0,
                      focuscolor="none",
                      relief="flat",
                      padding=(20, 10))
        
        style.map("Modern.TButton",
                 background=[('active', hover_color),
                           ('pressed', hover_color)])
        
        # Primary action button (larger, more prominent)
        style.configure("Primary.TButton",
                      background=bg_color,
                      foreground=cls.TEXT_PRIMARY,
                      borderwidth=0,
                      focuscolor="none",
                      relief="flat",
                      padding=(30, 15),
                      font=('Segoe UI', 10, 'bold'))
        
        style.map("Primary.TButton",
                 background=[('active', hover_color),
                           ('pressed', hover_color)])
    
    @classmethod
    def _configure_entry_combobox(cls, style, field_bg, border_color, arrow_color):
        """Configure entry and combobox styles"""
        # Modern entry style
        style.configure("Modern.TEntry",
                      fieldbackground=field_bg,
                      borderwidth=1,
                      relief="solid",
                      bordercolor=border_color,
                      insertcolor=cls.TEXT_PRIMARY,
                      padding=(10, 8))
        
        style.map("Modern.TEntry",
                 bordercolor=[('focus', cls.ACCENT)])
        
        # Modern combobox style
        style.configure("Modern.TCombobox",
                      fieldbackground=field_bg,
                      borderwidth=1,
                      relief="solid",
                      bordercolor=border_color,
                      arrowcolor=arrow_color,
                      padding=(10, 8))
        
        style.map("Modern.TCombobox",
                 bordercolor=[('focus', cls.ACCENT)])
    
    @classmethod
    def _configure_labels(cls, style, bg_color, text_primary, text_secondary):
        """Configure label styles"""
        style.configure("Heading.TLabel",
                      background=bg_color,
                      foreground=text_primary,
                      font=('Segoe UI', 12, 'bold'))
        
        style.configure("Subheading.TLabel",
                      background=bg_color,
                      foreground=text_secondary,
                      font=('Segoe UI', 9))
    
    @classmethod
    def _configure_checkbutton(cls, style, bg_color, text_color):
        """Configure checkbutton style"""
        style.configure("Modern.TCheckbutton",
                      background=bg_color,
                      foreground=text_color,
                      focuscolor="none",
                      font=('Segoe UI', 9))
    
    @classmethod
    def _configure_status_labels(cls, style, bg_color):
        """Configure status label styles"""
        style.configure("Success.TLabel",
                      background=bg_color,
                      foreground=cls.SUCCESS,
                      font=('Segoe UI', 9))
        
        style.configure("Warning.TLabel",
                      background=bg_color,
                      foreground=cls.WARNING,
                      font=('Segoe UI', 9))
        
        style.configure("Error.TLabel",
                      background=bg_color,
                      foreground=cls.ERROR,
                      font=('Segoe UI', 9))
    
    @classmethod
    def _configure_light_device_dropdown(cls, style):
        """Configure light-themed device dropdown (always light regardless of theme)"""
        style.configure("LightDevice.TCombobox",
                      fieldbackground=cls.LIGHT_CARD_BG,
                      background=cls.LIGHT_CARD_BG,
                      foreground=cls.LIGHT_TEXT_PRIMARY,
                      borderwidth=1,
                      relief="solid",
                      bordercolor=cls.LIGHT_BORDER,
                      arrowcolor=cls.LIGHT_TEXT_SECONDARY,
                      selectbackground=cls.ACCENT,
                      selectforeground="#ffffff",
                      padding=(10, 8))
        
        style.map("LightDevice.TCombobox",
                 fieldbackground=[('readonly', cls.LIGHT_CARD_BG)],
                 background=[('readonly', cls.LIGHT_CARD_BG)],
                 foreground=[('readonly', cls.LIGHT_TEXT_PRIMARY)],
                 bordercolor=[('focus', cls.ACCENT)])
    
    @classmethod
    def get_theme_colors(cls, theme="dark"):
        """Get theme colors dictionary"""
        if theme == "dark":
            return {
                'bg': cls.DARK_BG,
                'card_bg': cls.CARD_BG,
                'darker_bg': cls.DARKER_BG,
                'text_primary': cls.TEXT_PRIMARY,
                'text_secondary': cls.TEXT_SECONDARY,
                'border': cls.BORDER,
                'accent': cls.ACCENT,
                'success': cls.SUCCESS,
                'warning': cls.WARNING,
                'error': cls.ERROR
            }
        else:
            return {
                'bg': cls.LIGHT_BG,
                'card_bg': cls.LIGHT_CARD_BG,
                'darker_bg': cls.LIGHT_CARD_BG,
                'text_primary': cls.LIGHT_TEXT_PRIMARY,
                'text_secondary': cls.LIGHT_TEXT_SECONDARY,
                'border': cls.LIGHT_BORDER,
                'accent': cls.ACCENT,
                'success': cls.SUCCESS,
                'warning': cls.WARNING,
                'error': cls.ERROR
            }