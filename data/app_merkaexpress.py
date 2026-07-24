import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from datetime import datetime
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns

class AplicacionEmpresarial(tk.Tk):
    """Enrutador Principal (Contenedor de Módulos)"""
    def __init__(self, ruta_csv):
        super().__init__()
        self.ruta_csv = ruta_csv
        
        self.title("NexoTech - Sistema Integrado POS/ERP/SCM/CRM")
        self.geometry("1200x750")
        self.configure(bg="#f4f4f4")
        
        self.container = tk.Frame(self, bg="#f4f4f4")
        self.container.pack(fill="both", expand=True)
        
        self.frames = {}
        
        # Cargamos todas las interfaces, ahora incluyendo el ModuloCRM
        for F in (MenuPrincipal, ModuloTPS, ModuloSCM, ModuloERP, ModuloCRM, ModuloBI):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            
        self.mostrar_frame(MenuPrincipal)
        
    def mostrar_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        # Actualizar datos al entrar a módulos de lectura
        if cont in [ModuloBI, ModuloSCM, ModuloERP, ModuloCRM]:
            frame.actualizar_datos()

class MenuPrincipal(tk.Frame):
    """Interfaz del Menú Principal"""
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f4f4f4")
        self.controller = controller
        
        lbl_title = tk.Label(self, text="SISTEMA INTEGRADO EMPRESARIAL", font=("Arial", 22, "bold"), bg="#f4f4f4", fg="#333")
        lbl_title.pack(pady=40)
        
        lbl_subtitle = tk.Label(self, text="Seleccione el módulo al que desea acceder:", font=("Arial", 14), bg="#f4f4f4", fg="#666")
        lbl_subtitle.pack(pady=10)
        
        btn_tps = tk.Button(self, text="1. Módulo TPS (Punto de Venta)", font=("Arial", 14), width=45, bg="#2c7fb8", fg="white", cursor="hand2", command=lambda: controller.mostrar_frame(ModuloTPS))
        btn_tps.pack(pady=10)
        
        btn_scm = tk.Button(self, text="2. Módulo SCM (Inventario)", font=("Arial", 14), width=45, bg="#1b9e77", fg="white", cursor="hand2", command=lambda: controller.mostrar_frame(ModuloSCM))
        btn_scm.pack(pady=10)
        
        btn_erp = tk.Button(self, text="3. Módulo ERP (Finanzas)", font=("Arial", 14), width=45, bg="#7570b3", fg="white", cursor="hand2", command=lambda: controller.mostrar_frame(ModuloERP))
        btn_erp.pack(pady=10)
        
        # BOTÓN CRM ACTIVADO
        btn_crm = tk.Button(self, text="4. Módulo CRM (Clientes)", font=("Arial", 14), width=45, bg="#e7298a", fg="white", cursor="hand2", command=lambda: controller.mostrar_frame(ModuloCRM))
        btn_crm.pack(pady=10)
        
        btn_bi = tk.Button(self, text="5. Tablero Gerencial (Dashboards)", font=("Arial", 14), width=45, bg="#d95f02", fg="white", cursor="hand2", command=lambda: controller.mostrar_frame(ModuloBI))
        btn_bi.pack(pady=10)

class ModuloTPS(tk.Frame):
    """Interfaz del Módulo TPS (Transacciones)"""
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#ffffff")
        self.controller = controller
        self.ruta_csv = controller.ruta_csv
        
        try:
            self.df = pd.read_csv(self.ruta_csv)
            # Extraemos todas las ciudades dinámicamente
            self.ciudades = self.df['City'].unique().tolist()
            self.lineas_producto = self.df['Product line'].unique().tolist()
        except Exception:
            self.ciudades = ["Sin datos"]
            self.lineas_producto = ["Sin datos"]
            
        lbl_title = tk.Label(self, text="MÓDULO TPS - CAJA REGISTRADORA", font=("Arial", 18, "bold"), bg="#ffffff", fg="#2ca25f")
        lbl_title.pack(pady=20)
        
        form_frame = tk.Frame(self, bg="#ffffff")
        form_frame.pack(pady=20)
        
        tk.Label(form_frame, text="Sucursal (Ciudad):", font=("Arial", 12), bg="#ffffff").grid(row=0, column=0, padx=10, pady=15, sticky="e")
        self.cmb_ciudad = ttk.Combobox(form_frame, values=self.ciudades, font=("Arial", 12), state="readonly", width=25)
        self.cmb_ciudad.grid(row=0, column=1, padx=10, pady=15)
        if self.ciudades: self.cmb_ciudad.current(0)
        
        tk.Label(form_frame, text="Línea de Producto:", font=("Arial", 12), bg="#ffffff").grid(row=1, column=0, padx=10, pady=15, sticky="e")
        self.cmb_producto = ttk.Combobox(form_frame, values=self.lineas_producto, font=("Arial", 12), state="readonly", width=25)
        self.cmb_producto.grid(row=1, column=1, padx=10, pady=15)
        if self.lineas_producto: self.cmb_producto.current(0)
        
        tk.Label(form_frame, text="Cantidad a Vender:", font=("Arial", 12), bg="#ffffff").grid(row=2, column=0, padx=10, pady=15, sticky="e")
        self.ent_cantidad = tk.Entry(form_frame, font=("Arial", 12), width=27, relief="solid")
        self.ent_cantidad.grid(row=2, column=1, padx=10, pady=15)
        
        tk.Label(form_frame, text="Precio Unitario ($):", font=("Arial", 12), bg="#ffffff").grid(row=3, column=0, padx=10, pady=15, sticky="e")
        self.ent_precio = tk.Entry(form_frame, font=("Arial", 12), width=27, relief="solid")
        self.ent_precio.grid(row=3, column=1, padx=10, pady=15)
        
        btn_procesar = tk.Button(self, text="Procesar Transacción", font=("Arial", 12, "bold"), bg="#2ca25f", fg="white", cursor="hand2", command=self.procesar_venta)
        btn_procesar.pack(pady=15)
        
        btn_volver = tk.Button(self, text="<< Volver al Menú Principal", font=("Arial", 11), cursor="hand2", command=lambda: controller.mostrar_frame(MenuPrincipal))
        btn_volver.pack(pady=10)
        
    def procesar_venta(self):
        try:
            ciudad = self.cmb_ciudad.get()
            producto = self.cmb_producto.get()
            cantidad = int(self.ent_cantidad.get())
            # Forzamos conversión a entero para cálculos estrictos
            precio = int(self.ent_precio.get()) 
            
            cogs = int(precio * cantidad)
            tax = int(cogs * 0.05)
            sales = int(cogs + tax)
            margin_pct = int((tax / sales) * 100) if sales > 0 else 0
            
            resumen = f"Sucursal:\t{ciudad}\nProducto:\t{producto} x{cantidad}\n\nSubtotal (COGS):\t${cogs}\nImpuestos (5%):\t${tax}\nTOTAL A PAGAR:\t${sales}"
            
            respuesta = messagebox.askyesno("Confirmar Transacción", resumen + "\n\n¿Desea facturar y guardar en la Base de Datos?")
            
            if respuesta:
                self.df = pd.read_csv(self.ruta_csv)
                fecha_actual = self.df['Date'].max() if not self.df.empty else datetime.now().strftime('%m/%d/%Y')
                nuevo_registro = {
                    'Invoice ID': f"TPS-{int(time.time())}", 'Branch': 'A', 'City': ciudad,
                    'Customer type': 'Normal', 'Gender': 'Female', 'Product line': producto,
                    'Unit price': precio, 'Quantity': cantidad, 'Tax 5%': tax, 'Sales': sales,
                    'Date': fecha_actual, 'Time': datetime.now().strftime('%H:%M:%S'),
                    'Payment': 'Ewallet', 'cogs': cogs, 'gross margin percentage': margin_pct,
                    'gross income': tax, 'Rating': 9
                }
                self.df = pd.concat([self.df, pd.DataFrame([nuevo_registro])], ignore_index=True)
                self.df.to_csv(self.ruta_csv, index=False)
                
                messagebox.showinfo("Transacción Exitosa", "La venta ha sido registrada exitosamente.\n\nSe han actualizado los módulos SCM, ERP y CRM automáticamente.")
                self.ent_cantidad.delete(0, tk.END)
                self.ent_precio.delete(0, tk.END)
                
        except ValueError:
            messagebox.showerror("Error de Datos", "Ingrese valores numéricos enteros válidos en Cantidad y Precio.")

class ModuloSCM(tk.Frame):
    """Interfaz del Módulo SCM (Inventario)"""
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#ffffff")
        self.controller = controller
        
        lbl_title = tk.Label(self, text="MÓDULO SCM - CONTROL DE INVENTARIO", font=("Arial", 18, "bold"), bg="#ffffff", fg="#1b9e77")
        lbl_title.pack(pady=20)
        
        columns = ("Línea de Producto", "Unidades Totales Vendidas", "Estado de Reorden")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=12)
        self.tree.heading("Línea de Producto", text="Línea de Producto")
        self.tree.heading("Unidades Totales Vendidas", text="Unidades Totales Vendidas")
        self.tree.heading("Estado de Reorden", text="Estado de Reorden")
        self.tree.column("Unidades Totales Vendidas", anchor=tk.CENTER)
        self.tree.column("Estado de Reorden", anchor=tk.CENTER)
        self.tree.pack(pady=20, padx=40, fill=tk.X)
        
        btn_volver = tk.Button(self, text="<< Volver al Menú Principal", font=("Arial", 11), cursor="hand2", command=lambda: controller.mostrar_frame(MenuPrincipal))
        btn_volver.pack(pady=10)

    def actualizar_datos(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        try:
            df = pd.read_csv(self.controller.ruta_csv)
            productos_vendidos = df.groupby('Product line')['Quantity'].sum().sort_values(ascending=False).reset_index()
            
            for index, row in productos_vendidos.iterrows():
                estado = "Órden Automática Generada" if int(row['Quantity']) > 900 else "Stock Estable"
                self.tree.insert("", tk.END, values=(row['Product line'], int(row['Quantity']), estado))
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el inventario: {e}")

class ModuloERP(tk.Frame):
    """Interfaz del Módulo ERP (Finanzas)"""
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#ffffff")
        self.controller = controller
        
        lbl_title = tk.Label(self, text="MÓDULO ERP - FINANZAS Y CONTABILIDAD", font=("Arial", 18, "bold"), bg="#ffffff", fg="#7570b3")
        lbl_title.pack(pady=20)
        
        self.frame_kpis = tk.Frame(self, bg="#ffffff")
        self.frame_kpis.pack(pady=30)
        
        self.lbl_ventas = tk.Label(self.frame_kpis, text="Ingresos Totales:\n$0", font=("Arial", 16, "bold"), bg="#e6f2ff", width=20, height=3, relief="groove")
        self.lbl_ventas.grid(row=0, column=0, padx=20)
        
        self.lbl_cogs = tk.Label(self.frame_kpis, text="Costo de Ventas:\n$0", font=("Arial", 16, "bold"), bg="#fcecec", width=20, height=3, relief="groove")
        self.lbl_cogs.grid(row=0, column=1, padx=20)
        
        self.lbl_tax = tk.Label(self.frame_kpis, text="Impuestos (5%):\n$0", font=("Arial", 16, "bold"), bg="#e6ffe6", width=20, height=3, relief="groove")
        self.lbl_tax.grid(row=0, column=2, padx=20)
        
        btn_volver = tk.Button(self, text="<< Volver al Menú Principal", font=("Arial", 11), cursor="hand2", command=lambda: controller.mostrar_frame(MenuPrincipal))
        btn_volver.pack(pady=40)

    def actualizar_datos(self):
        try:
            df = pd.read_csv(self.controller.ruta_csv)
            ventas_totales = int(df['Sales'].sum())
            cogs_totales = int(df['cogs'].sum())
            impuestos_totales = int(df['Tax 5%'].sum())
            
            self.lbl_ventas.config(text=f"Ingresos Totales (Sales):\n${ventas_totales}")
            self.lbl_cogs.config(text=f"Costo de Ventas (COGS):\n${cogs_totales}")
            self.lbl_tax.config(text=f"Impuestos Recaudados:\n${impuestos_totales}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la contabilidad: {e}")

class ModuloCRM(tk.Frame):
    """Interfaz del Módulo CRM (Control y Retención de Clientes)"""
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#ffffff")
        self.controller = controller
        
        lbl_title = tk.Label(self, text="MÓDULO CRM - AUDITORÍA DE CLIENTES", font=("Arial", 18, "bold"), bg="#ffffff", fg="#e7298a")
        lbl_title.pack(pady=20)
        
        columns = ("Perfil Demográfico", "Días de Inactividad", "Estado de Retención")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=12)
        self.tree.heading("Perfil Demográfico", text="Perfil Demográfico (Tipo | Ciudad | Género)")
        self.tree.heading("Días de Inactividad", text="Días de Inactividad")
        self.tree.heading("Estado de Retención", text="Estado de Retención")
        self.tree.column("Perfil Demográfico", anchor=tk.W, width=350)
        self.tree.column("Días de Inactividad", anchor=tk.CENTER, width=150)
        self.tree.column("Estado de Retención", anchor=tk.CENTER, width=250)
        self.tree.pack(pady=20, padx=40, fill=tk.X)
        
        btn_volver = tk.Button(self, text="<< Volver al Menú Principal", font=("Arial", 11), cursor="hand2", command=lambda: controller.mostrar_frame(MenuPrincipal))
        btn_volver.pack(pady=10)

    def actualizar_datos(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        try:
            df = pd.read_csv(self.controller.ruta_csv)
            df['Date'] = pd.to_datetime(df['Date'])
            fecha_actual = df['Date'].max()
            
            # Clasificación de clientes según su perfil demográfico
            df['Perfil_Cliente'] = df['Customer type'] + " | " + df['City'] + " | " + df['Gender']
            perfiles = df.groupby('Perfil_Cliente')['Date'].max().reset_index()
            
            umbral_dias = 25
            
            for index, row in perfiles.iterrows():
                # Días calculados estrictamente como número entero
                dias_inactivos = int((fecha_actual - row['Date']).days)
                estado = "¡ALERTA DE DESERCIÓN!" if dias_inactivos >= umbral_dias else "Cliente Activo"
                
                self.tree.insert("", tk.END, values=(row['Perfil_Cliente'], dias_inactivos, estado))
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo auditar la base de clientes: {e}")

class ModuloBI(tk.Frame):
    """Interfaz del Tablero Gerencial de Inteligencia de Negocios"""
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#ffffff")
        self.controller = controller
        
        lbl_title = tk.Label(self, text="TABLERO GERENCIAL - DASHBOARDS", font=("Arial", 18, "bold"), bg="#ffffff", fg="#d95f02")
        lbl_title.pack(pady=10)
        
        self.canvas_frame = tk.Frame(self, bg="#ffffff")
        self.canvas_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        btn_volver = tk.Button(self, text="<< Volver al Menú Principal", font=("Arial", 11), cursor="hand2", command=lambda: controller.mostrar_frame(MenuPrincipal))
        btn_volver.pack(pady=10)
        
        self.canvas_widget = None

    def actualizar_datos(self):
        try:
            df = pd.read_csv(self.controller.ruta_csv)
            df['Date'] = pd.to_datetime(df['Date'])
            
            ventas_semanales = df.resample('W', on='Date')['Sales'].sum().reset_index()
            
            df['Perfil_Cliente'] = df['Customer type'] + " | " + df['City'] + " | " + df['Gender']
            fecha_actual = df['Date'].max()
            rfm = df.groupby('Perfil_Cliente').agg({
                'Date': lambda x: (fecha_actual - x.max()).days,
                'Invoice ID': 'count',
                'Sales': 'sum'
            }).reset_index()
            rfm.columns = ['Perfil_Cliente', 'Recency', 'Frequency', 'Monetary']
            rfm['R_Score'] = pd.qcut(rfm['Recency'].rank(method='first'), 4, labels=[4, 3, 2, 1])
            rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 4, labels=[1, 2, 3, 4])
            
            def clasificar_segmento(row):
                r, f = int(row['R_Score']), int(row['F_Score'])
                if r >= 3 and f >= 3: return "VIP"
                elif r >= 3 and f < 3: return "Promedio"
                elif r < 3 and f >= 3: return "Recuperable"
                else: return "En Riesgo"
                
            rfm['Etiqueta_Estrategica'] = rfm.apply(clasificar_segmento, axis=1)
            segmentos_conteo = rfm['Etiqueta_Estrategica'].value_counts()
            
            productos_vendidos = df.groupby('Product line')['Quantity'].sum().sort_values(ascending=False).reset_index()

            if self.canvas_widget:
                self.canvas_widget.destroy()

            sns.set_theme(style="whitegrid")
            fig, axes = plt.subplots(1, 3, figsize=(15, 4))
            fig.subplots_adjust(bottom=0.25, top=0.85, wspace=0.3)
            
            sns.lineplot(data=ventas_semanales, x='Date', y='Sales', ax=axes[0], color='#2c7fb8', marker='o')
            axes[0].set_title('Evolución Ventas (Semanal)', fontsize=10, fontweight='bold')
            axes[0].tick_params(axis='x', rotation=30, labelsize=8)
            axes[0].set_xlabel('')
            axes[0].set_ylabel('Ventas ($)', fontsize=9)
            
            axes[1].pie(segmentos_conteo, labels=segmentos_conteo.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette("pastel"))
            axes[1].set_title('Segmentación RFM', fontsize=10, fontweight='bold')
            
            sns.barplot(data=productos_vendidos, x='Quantity', y='Product line', ax=axes[2], palette="viridis", hue='Product line', legend=False)
            axes[2].set_title('KPI SCM: Unidades por Línea', fontsize=10, fontweight='bold')
            axes[2].set_xlabel('Cant. Vendida', fontsize=9)
            axes[2].set_ylabel('')
            axes[2].tick_params(axis='y', labelsize=8)

            canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
            canvas.draw()
            self.canvas_widget = canvas.get_tk_widget()
            self.canvas_widget.pack(fill=tk.BOTH, expand=True)
            
        except Exception as e:
            messagebox.showerror("Error", f"Fallo al generar dashboards:\n{e}")

if __name__ == "__main__":
    archivo_base = 'SuperMarket Analysis.csv'
    app = AplicacionEmpresarial(archivo_base)
    app.mainloop()