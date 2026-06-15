import tkinter as tk
from tkinter import Listbox, Canvas, Tk, END
from tkinter import LEFT, TOP, BOTTOM, W, X, Y, NW, BOTH, HORIZONTAL, SUNKEN
from tkinter.ttk import Entry, Button, Frame, Label, Progressbar 

from PIL import Image, ImageTk
from io import BytesIO
from urllib.parse import urljoin

from helpers import get_img_urls, get_img_data
from aiohttp import ClientSession

import asyncio

from rx.subject import Subject
from rx import operators as ops
from rx.scheduler.mainloop import TkinterScheduler

class App():

    def __init__(self, root):
        self.root = root
        self.root.title("Practice 2")
        self.root.geometry("1200x800")

        self.urls_data = {}

        self.scheduler = TkinterScheduler(self.root)
        self.image_subject = Subject()
        self.image_subject.pipe(
            ops.observe_on(self.scheduler),
            ops.filter(lambda item: item['data'] is not None)
        ).subscribe(
            on_next=self.on_image_downloaded,
            on_error=self.on_download_error,
            on_completed=self.on_download_complete
        )

        # Top frame
        top_frame = Frame(root, padding="10 10 10 5")
        top_frame.pack(side=TOP, fill=X)

        Label(top_frame, text="URL to process:").pack(side=LEFT, padx=(0, 5))

        self.url_entry = Entry(top_frame)
        self.url_entry.pack(side=LEFT, fill=X, expand=True, padx=(0, 5))

        self.process_btn = Button(top_frame, text="Process", command=self.on_process)
        self.process_btn.pack(side=LEFT)

        # Bottom frame 
        bottom_frame = Frame(root, padding="10 5 10 10")
        bottom_frame.pack(side=BOTTOM, fill=X)

        self.status_label = Label(bottom_frame, text="Status: Ready")
        self.status_label.pack(side=TOP, anchor=W, pady=(0, 5))
        
        self.progress = Progressbar(bottom_frame, orient=HORIZONTAL, mode='determinate')
        self.progress.pack(side=TOP, fill=X)

        # Middle frame 
        middle_frame = Frame(root, padding="10 5 10 5")
        middle_frame.pack(side=TOP, fill=BOTH, expand=True)

        # Left frame
        left_panel = Frame(middle_frame, relief=SUNKEN, width=200)
        left_panel.pack(side=LEFT, fill=Y, padx=(0, 10))

        self.listbox = Listbox(left_panel)
        self.listbox.pack(fill=BOTH, expand=True, padx=5, pady=5)
        self.listbox.bind('<<ListboxSelect>>', self.on_listbox_select)
        
        # Main Area (Image Rendering)
        main_area = Frame(middle_frame, relief=SUNKEN)
        main_area.pack(side=LEFT, fill=BOTH, expand=True)

        self.image_canvas = Canvas(main_area, bg="gray")
        self.image_canvas.pack(fill=BOTH, expand=True, padx=5, pady=5)


    def on_process(self):
        url = self.url_entry.get().strip()
        if not url: return

        self.status_label.config(text=f"Status: Fetching URLs from {url}...")
        self.listbox.delete(0, END)
        self.urls_data.clear()
        self.progress['value'] = 0

        asyncio.create_task(self.download_images_task(url))


    async def download_images_task(self, base_url):
        try:
            async with ClientSession() as sesh:
                images_to_process = await get_img_urls(sesh, base_url)
                
                if not images_to_process:
                    self.image_subject.on_completed()
                    return

                self.status_label.config(text=f"{len(images_to_process)} images found")
                self.progress_step = 100.0 / len(images_to_process)

                tasks = [self.fetch_and_notify(sesh, img) for img in images_to_process]
                await asyncio.gather(*tasks)

                self.image_subject.on_completed()
        except Exception as e: self.image_subject.on_error(e)


    async def fetch_and_notify(self, sesh, img_info):
        try:
            data = await get_img_data(sesh, img_info['url'])
            self.image_subject.on_next({
                'name': img_info['name'],
                'data': data
            })
        except Exception as e:
            print(f"Failed to fetch {img_info['url']}: {e}")


    def on_image_downloaded(self, item):
        img_name = item['name']
        img_data = item['data']
        
        # Save data using the name as the key so we can retrieve it when clicked
        self.urls_data[img_name] = img_data
        
        # Add the extracted NAME to the left menu, not the URL
        self.listbox.insert(END, img_name)
        
        # Update progress bar
        self.progress['value'] += self.progress_step

    def on_download_error(self, error):
        self.status_label.config(text=f"Status: Error - {error}")

    def on_download_complete(self):
        self.progress['value'] = 100

    def on_listbox_select(self, event):
        # Render the image when selected from the list
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            name = self.listbox.get(index)
            data = self.urls_data.get(name)
            if data:
                self.render_img(data)

    def render_img(self, img_data):
        try:
            pil_img = Image.open(BytesIO(img_data))
            # Resize image to fit canvas for better viewability (optional)
            pil_img.thumbnail((800, 600), Image.Resampling.LANCZOS)
            
            # Save reference to prevent garbage collection!
            self.img_tk = ImageTk.PhotoImage(pil_img)
            
            self.image_canvas.delete('all') 
            self.image_canvas.create_image(0, 0, anchor=NW, image=self.img_tk)
        except Exception as e:
            print(f"Error rendering image: {e}")


async def gui_loop(root):
    while True:
        try:
            root.update()
            await asyncio.sleep(0.01)
        except tk.TclError: break


async def main():
    root = Tk()
    app = App(root)
    await gui_loop(root)


if __name__ == "__main__":
    asyncio.run(main())
