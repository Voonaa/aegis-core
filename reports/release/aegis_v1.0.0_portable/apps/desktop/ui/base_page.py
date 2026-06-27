"""Base page template class structure for Aegis Toolkit viewports."""

import customtkinter as ctk

class BasePage(ctk.CTkFrame):
    """Abstract interface frame for page views enforcing standard lifecycle hooks."""

    def __init__(self, master: any, **kwargs: any) -> None:
        """Initialize the Base Page.
        
        Args:
            master: Parent container frame.
            kwargs: Visual style parameters for CTkFrame.
        """
        super().__init__(master=master, corner_radius=0, fg_color="transparent", **kwargs)

    def show(self) -> None:
        """Visual display method gridding page into container viewport."""
        self.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        self.on_enter()

    def hide(self) -> None:
        """Visual hide method forgetting page from viewport grid layouts."""
        self.on_leave()
        self.grid_forget()

    def on_enter(self) -> None:
        """Fires when page enters active view viewport. Call data resumes."""
        self.on_resume()

    def on_leave(self) -> None:
        """Fires when page leaves active view. Call data pauses."""
        self.on_pause()

    def on_resume(self) -> None:
        """Resumes telemetry timers or hooks. Overridden by subclasses."""
        pass

    def on_pause(self) -> None:
        """Pauses telemetry timers or hooks. Overridden by subclasses."""
        pass
