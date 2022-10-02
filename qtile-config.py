from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

import os
import subprocess

mod = "mod4"
terminal = guess_terminal()

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "Left", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "Right", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "Down", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "Up", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "Left", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "Right", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "Left", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "Right", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "Down", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "Up", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.spawn('firefox'), desc="Launch web browser"),
    Key([mod], "c", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "shift"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "d", lazy.spawn('rofi -show drun'), desc="Spawn a command using ROFI"),
    Key([mod], "n", lazy.spawn('thunar'), desc="Open file manager"),

    Key([mod, "shift"], "p", lazy.spawn('poweroff now'), desc="Shutdown RIGHT NOW"),
    Key([mod, "shift"], "s", lazy.spawn('flameshot gui'), desc="Take screenshot"),

    Key([], "XF86MonBrightnessUp", lazy.spawn('xbacklight -inc 5'), desc="Brightness up"),
    Key([], "XF86MonBrightnessDown", lazy.spawn('xbacklight -dec 5'), desc="Brightness down"),
    Key([], "XF86AudioRaiseVolume", lazy.spawn('amixer set Master 5%+ -q'), desc="Volume up"),
    Key([], "XF86AudioLowerVolume", lazy.spawn('amixer set Master 5%- -q'), desc="Volume down"),
    Key([], "XF86AudioMute", lazy.spawn('amixer -q set Master toggle'), desc="Mute/Unmute"),
    Key([], "XF86AudioPlay", lazy.spawn('playerctl play-pause'), desc='Play/Pause'),
    Key([], "XF86AudioNext", lazy.spawn('playerctl next'), desc='Next Audio'),
    Key([], "XF86AudioPrev", lazy.spawn('playerctl previous'), desc='Prev Audio')
]

groups = [Group(i) for i in "一二三四五六七八九"]

#groups = [Group(i) for i in "123456789"]

for idx, i in enumerate(groups, start=1):
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                str(idx),
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(idx),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                str(idx),
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(idx),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

colors = ["#f66a78","#7a2728", "#b93b3e", "#566c2e", "#6b8429", "#89ac32", "#e3ca69", "#f86375", "#b14b55", "#404036"]
bar_bg_color = "#1A1B26"

layouts = [
    layout.Columns(
        border_focus = colors[2],
        border_focus_stack = colors[5],
        border_normal = bar_bg_color,
        border_normal_stack = bar_bg_color,
        fair = True,
        margin = 3,
        margin_on_single = 0,
        ),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font='DejaVu Sans mono for powerline',
    fontsize=13,
    padding=10,
)
extension_defaults = widget_defaults.copy()

def slash(lcolor, rcolor):
    return widget.TextBox(
            text='\ue0be',
            font='Inconsolata for powerline',
            fontsize=33,
            padding=0,
            background=rcolor,
            foreground=lcolor)

def backslash(lcolor, rcolor):
    return widget.TextBox(
            text='\ue0bc',
            font='Inconsolata for powerline',
            fontsize=33,
            padding=0,
            background=lcolor,
            foreground=rcolor)

screens = [
    Screen(
        top=bar.Bar(
            [   
                slash(bar_bg_color, colors[0]),
                widget.GroupBox(
                    borderwidth=0,
                    active='787C99',
                    inactive='3B3D49',
                    disable_drag = True,
                    block_highlight_text_color = colors[0],
                    highlight_color = colors[0],
                    font="Noto Sans Bold",
                    highlight_method = bar_bg_color,
                    margin = 0
                ),
                widget.Spacer(length=5),
                slash(colors[1], bar_bg_color),
                widget.CurrentLayout(background=colors[1]),
                slash(colors[2], colors[1]),
                widget.Battery(
                    format='{percent:2.0%}',
                    background=colors[2],
                    fmt='  {}'
                ),
                slash(bar_bg_color, colors[2]),
                widget.WindowName(max_chars=200),

                backslash(colors[3], bar_bg_color),
                widget.CPU(
                    background=colors[3],
                    format='  {load_percent}%',
                ),
                backslash(colors[4], colors[3]),
                widget.ThermalSensor(
                    background=colors[4],
                    fmt='  {}',
                    format='{temp:.1f}{unit}'),
                #widget.DF(
                #    background=colors[4],
                #    fmt='  {}',
                #    partition='/',
                #    visible_on_warn=False,
                #    format='{f}{m}'
                #),
                backslash(colors[5], colors[4]),
                widget.Memory(
                    background=colors[5],
                    format='  {MemUsed: .0f}{mm}'
                ),
                backslash(colors[6], colors[5]),
                widget.Backlight(
                    backlight_name="intel_backlight",
                    fmt='  {}',
                    foreground='000000',
                    background=colors[6]),
                backslash(colors[7], colors[6]),
                widget.Volume(
                    foreground='000000',
                    background=colors[7],
                    fmt='  {}'
                    ),
                backslash(colors[8], colors[7]),
                widget.Clock(
                        format="%B %d, %H:%M",
                    background=colors[8],
                ),
                backslash(colors[9], colors[8]),
                widget.QuickExit(
                    default_text=' ',
                    countdown_format='{}',
                    background=colors[9]
                    )
            ],
            25,
            background=bar_bg_color,
            #border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            #border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.run([home])
