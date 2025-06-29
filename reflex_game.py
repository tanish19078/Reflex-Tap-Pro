import tkinter as tk
import random
import time
import os

class ReflexTapPro:
    def __init__(self, root):
        self.root = root
        self.root.title("⚡ Reflex Tap Pro")
        self.root.geometry("960x720")
        self.root.configure(bg="#101820")

        # Game config
        self.game_duration = 30
        self.remaining_time = self.game_duration
        self.reaction_times = []
        self.total_score = 0
        self.clicks = 0
        self.combo = 0
        self.high_score = self.load_high_score()
        self.running = True

        # UI Setup
        self.header = tk.Label(root, text="⚡ Reflex Tap Pro", fg="#f2aa4c", bg="#101820",
                               font=("Verdana", 32, "bold"))
        self.header.pack(pady=20)

        self.stats_frame = tk.Frame(root, bg="#101820")
        self.stats_frame.pack(pady=10)

        self.stats = tk.Label(self.stats_frame, text="", fg="#f2aa4c", bg="#101820", font=("Courier New", 16))
        self.stats.pack()

        self.combo_label = tk.Label(root, text="", fg="#ffcc00", bg="#101820", font=("Verdana", 16, "italic"))
        self.combo_label.pack(pady=10)

        self.highscore_label = tk.Label(root, text=f"🏆 High Score: {self.high_score}", fg="#e0e0e0",
                                        bg="#101820", font=("Verdana", 16, "bold"))
        self.highscore_label.pack(pady=10)

        self.button = tk.Button(root, text="", font=("Verdana", 16), command=self.handle_click,
                                relief="raised", bd=4)
        self.button.place_forget()

        self.update_stats()
        self.start_game_loop()
        self.root.after(1000, self.timer_tick)

    def load_high_score(self):
        if os.path.exists("highscore.txt"):
            with open("highscore.txt", "r") as f:
                return int(f.read())
        return 0

    def save_high_score(self):
        with open("highscore.txt", "w") as f:
            f.write(str(self.high_score))

    def update_stats(self):
        avg_time = sum(self.reaction_times) / len(self.reaction_times) if self.reaction_times else 0
        self.stats.config(
            text=f"⏳ Time: {self.remaining_time}s   🎯 Score: {self.total_score}   🖱️ Clicks: {self.clicks}   ⚡ Avg: {avg_time:.3f}s"
        )

    def timer_tick(self):
        if not self.running:
            return

        self.remaining_time -= 1
        self.update_stats()

        if self.remaining_time <= 0:
            self.end_game()
        else:
            self.root.after(1000, self.timer_tick)

    def start_game_loop(self):
        if not self.running:
            return

        self.spawn_button()
        speed = max(600, 3000 - (30 - self.remaining_time) * 100)
        self.root.after(speed, self.start_game_loop)

    def spawn_button(self):
        self.button.place_forget()

        is_trap = random.random() < 0.2
        x = random.randint(100, 800)
        y = random.randint(150, 600)
        size = max(10, 20 + self.remaining_time)

        self.task = "Trap" if is_trap else "Tap"
        self.start_time = time.time()

        self.button.place(x=x, y=y, width=size * 6, height=size * 2)
        self.button.config(
            text="DO NOT CLICK!" if is_trap else "TAP ME!",
            bg="#c1292e" if is_trap else "#1b98e0",
            fg="white" if is_trap else "black",
            activebackground="#f2aa4c",
            activeforeground="black"
        )

    def handle_click(self):
        if not self.running:
            return

        reaction_time = time.time() - self.start_time
        self.reaction_times.append(reaction_time)
        self.clicks += 1

        if self.task == "Trap":
            self.total_score -= 10
            self.combo = 0
            self.combo_label.config(text="")
            self.header.config(text="💥 That was a trap!")
        else:
            score = self.calculate_score(reaction_time)
            self.total_score += score
            self.combo += 1
            if self.combo >= 3:
                bonus = self.combo * 2
                self.total_score += bonus
                self.combo_label.config(text=f"🔥 Combo x{self.combo}! Bonus +{bonus}")
            else:
                self.combo_label.config(text="")
            self.header.config(text=f"✅ Great! {reaction_time:.3f}s")

        self.update_stats()
        self.button.place_forget()

    def calculate_score(self, rt):
        if rt < 0.4:
            return 10
        elif rt < 0.8:
            return 7
        elif rt < 1.2:
            return 5
        else:
            return 3

    def end_game(self):
        self.running = False
        self.button.place_forget()
        avg_time = sum(self.reaction_times) / len(self.reaction_times) if self.reaction_times else 0
        if self.total_score > self.high_score:
            self.high_score = self.total_score
            self.save_high_score()
        self.header.config(text=f"🏁 Final Score: {self.total_score}")
        self.stats.config(
            text=f"🎯 Clicks: {self.clicks}   ⚡ Avg Time: {avg_time:.3f}s   🏆 Score: {self.total_score}"
        )
        self.highscore_label.config(text=f"🏆 High Score: {self.high_score}")
        restart = tk.Button(self.root, text="🔁 Play Again", font=("Verdana", 14), bg="#f2aa4c", fg="black",
                            command=self.restart_game)
        restart.pack(pady=30)

    def restart_game(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.__init__(self.root)

# Run the game
root = tk.Tk()
game = ReflexTapPro(root)
root.mainloop()
