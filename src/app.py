#!/usr/bin/env python3
import sys, os, tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, Listbox, Scrollbar, END, MULTIPLE
import tkinter.ttk as ttk

try:
    from PyPDF2 import PdfMerger
    HAS_DEP = True
except ImportError:
    HAS_DEP = False

class App:
    def __init__(self, root):
        self.root = root
        root.title('PDF 合并工具 v1.0')
        root.geometry('700x500')
        self.files = []
        self.build_ui()
    
    def build_ui(self):
        f = tk.Frame(self.root, bg='#1f538d', height=60)
        f.pack(fill='x')
        tk.Label(f, text='PDF 合并工具', font=('Arial',16,'bold'), fg='white', bg='#1f538d').pack(pady=15)
        main = tk.Frame(self.root, padx=20, pady=15)
        main.pack(fill='both', expand=True)
        bf = tk.Frame(main)
        bf.pack(fill='x', pady=5)
        tk.Button(bf, text='添加PDF', command=self.add_files, bg='#1f538d', fg='white', padx=15).pack(side='left', padx=5)
        tk.Button(bf, text='移除选中', command=self.remove_sel, bg='#d9534f', fg='white', padx=15).pack(side='left', padx=5)
        tk.Button(bf, text='开始合并', command=self.merge, bg='#5cb85c', fg='white', font=('Arial',10,'bold'), padx=20).pack(side='right', padx=5)
        lf = tk.Frame(main)
        lf.pack(fill='both', expand=True)
        sb = Scrollbar(lf)
        sb.pack(side='right', fill='y')
        self.lb = Listbox(lf, selectmode=MULTIPLE, font=('Consolas',10), bg='#f8f9fa', selectbackground='#1f538d', yscrollcommand=sb.set, height=15)
        self.lb.pack(fill='both', expand=True)
        sb.config(command=self.lb.yview)
        self.status = tk.Label(main, text='请添加PDF文件', font=('Arial',10), fg='gray', anchor='w')
        self.status.pack(fill='x', pady=5)
    
    def add_files(self):
        fs = filedialog.askopenfilenames(title='选择PDF', filetypes=[('PDF','*.pdf')])
        for f in fs:
            if f not in self.files:
                self.files.append(f)
                self.lb.insert(END, Path(f).name)
        self.status.config(text=f'已添加 {len(self.files)} 个文件')
    
    def remove_sel(self):
        for i in sorted(list(self.lb.curselection()), reverse=True):
            del self.files[i]
        self.lb.delete(0, END)
        for f in self.files:
            self.lb.insert(END, Path(f).name)
        self.status.config(text=f'剩余 {len(self.files)} 个')
    
    def merge(self):
        if not self.files:
            messagebox.showwarning('提示', '请先添加PDF文件')
            return
        if not HAS_DEP:
            messagebox.showerror('缺少依赖', '请运行：pip install PyPDF2')
            return
        out = filedialog.asksaveasfilename(title='保存PDF', defaultextension='.pdf', filetypes=[('PDF','*.pdf')])
        if not out: return
        try:
            m = PdfMerger()
            for f in self.files: m.append(f)
            m.write(out)
            m.close()
            messagebox.showinfo('完成', f'成功合并 {len(self.files)} 个文件！')
        except Exception as e:
            messagebox.showerror('错误', str(e))

if __name__ == '__main__':
    root = tk.Tk()
    App(root)
    root.mainloop()
