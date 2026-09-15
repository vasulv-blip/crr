#!/usr/bin/env python3
"""
Generate a decluttered, modern, publication-grade System Architecture Block Diagram
for the Closed-Loop Cognitive Radio EW Simulation.
Designed for Shri S. K. Sir & Senior Defence Scientists.

Pure 3x2 Rectangular Closed-Loop Architecture:
- Top-Left: Hostile ECM Jammer (External Threat)
- Top-Center: Contested RF Propagation Medium
- Top-Right: ES Sensing Receiver
- Bottom-Right: Cognitive Decision Engine & ML Recommender
- Bottom-Center: Agile ECCM Transmitter
- Bottom-Left: System Data Bus Legend

All connecting buses are straight, orthogonal, unbroken lines with zero crossings.
All card content features clean numbered items (1 to 4) with generous spacing.
"""

import os
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as patches

BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"
OUT_PATH = ASSETS_DIR / "system_architecture_block_diagram.png"

def create_decluttered_diagram():
    # 17:9.6 widescreen canvas, 300 DPI for publication quality
    fig, ax = plt.subplots(figsize=(17, 9.6), dpi=300)
    ax.set_xlim(0, 17)
    ax.set_ylim(0, 9.6)
    ax.axis('off')
    fig.patch.set_facecolor('#FFFFFF')

    # Color Palette: Modern Defence C2 Palette
    C_RED_HDR    = '#B91C1C'  # Jammer (Adversary EA)
    C_RED_BDR    = '#EF4444'
    
    C_SLATE_HDR  = '#1E293B'  # Contested RF Medium
    C_SLATE_BDR  = '#64748B'
    
    C_BLUE_HDR   = '#0369A1'  # ES Sensing Receiver
    C_BLUE_BDR   = '#0284C7'
    
    C_GREEN_HDR  = '#15803D'  # Agile ECCM Transmitter
    C_GREEN_BDR  = '#16A34A'
    
    C_ENGINE_HDR = '#334155'  # Cognitive Decision Engine (Slate Steel C2)
    C_ENGINE_BDR = '#475569'
    
    C_NAVY_TITLE = '#0B2A5B'  # Top banner title

    # -------------------------------------------------------------
    # 1. TOP HEADER & METADATA BANNER
    # -------------------------------------------------------------
    ax.plot([0.8, 16.2], [9.35, 9.35], color=C_NAVY_TITLE, lw=2.5, solid_capstyle='round')
    
    ax.text(8.5, 9.06, 'CLOSED-LOOP COGNITIVE RADIO SYSTEM ARCHITECTURE', 
            ha='center', va='center', fontsize=15, fontweight='bold', color=C_NAVY_TITLE, fontfamily='sans-serif')
    ax.text(8.5, 8.78, 'Autonomous Sense-Decide-Act Closed Loop under Hostile EW · ES Spectrum Surveillance · Neural/Hybrid C2 · Agile ECCM Actuation', 
            ha='center', va='center', fontsize=8.8, fontstyle='italic', color='#475569', fontfamily='sans-serif')

    # -------------------------------------------------------------
    # 2. CARD DRAWING HELPER
    # Crisp white card body, sleek header, clean NUMBERED items
    # -------------------------------------------------------------
    def draw_card(ax, x, y, w, h, border_col, header_col, domain_tag, title, subtitle, items):
        # Subtle drop shadow
        shadow = patches.FancyBboxPatch((x + 0.04, y - 0.04), w, h, boxstyle='round,pad=0.01,rounding_size=0.14',
                                        facecolor='#E2E8F0', edgecolor='none', zorder=1)
        ax.add_patch(shadow)

        # Main Card Body
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.01,rounding_size=0.14',
                                      facecolor='#FFFFFF', edgecolor=border_col, linewidth=1.5, zorder=2)
        ax.add_patch(rect)
        
        # Header banner
        header_h = 0.76
        header_rect = patches.FancyBboxPatch((x, y + h - header_h), w, header_h, 
                                             boxstyle='round,pad=0.01,rounding_size=0.14',
                                             facecolor=header_col, edgecolor=header_col, linewidth=1, zorder=3)
        ax.add_patch(header_rect)
        
        # Square out bottom corners of header
        square_filler = patches.Rectangle((x, y + h - header_h), w, 0.35, 
                                          facecolor=header_col, edgecolor=header_col, linewidth=0, zorder=3)
        ax.add_patch(square_filler)

        # Domain Tag pill
        tag_w = len(domain_tag) * 0.068 + 0.36
        tag_box = patches.FancyBboxPatch((x + 0.22, y + h - 0.23), tag_w, 0.17,
                                         boxstyle='round,pad=0.01,rounding_size=0.06',
                                         facecolor=(1.0, 1.0, 1.0, 0.20),
                                         edgecolor='none', zorder=4)
        ax.add_patch(tag_box)
        ax.text(x + 0.22 + tag_w/2, y + h - 0.14, domain_tag, ha='center', va='center',
                fontsize=6.5, fontweight='bold', color='#FFFFFF', fontfamily='sans-serif', zorder=5)

        # Main Title & Subtitle
        ax.text(x + 0.22, y + h - 0.42, title, ha='left', va='center',
                fontsize=9.8, fontweight='bold', color='#FFFFFF', fontfamily='sans-serif', zorder=5)
        ax.text(x + 0.22, y + h - 0.61, subtitle, ha='left', va='center',
                fontsize=7.2, fontstyle='italic', color='#F1F5F9', fontfamily='sans-serif', zorder=5)

        # Divider line
        ax.plot([x, x + w], [y + h - header_h, y + h - header_h], color=border_col, lw=1.2, zorder=4)

        # Content: Numbered items (1., 2., 3., 4.) for clear structured legibility
        content_y = y + h - header_h - 0.36
        for num_idx, (lead, body) in enumerate(items, start=1):
            num_label = f"{num_idx}. "
            ax.text(x + 0.24, content_y, num_label, ha='left', va='center',
                    fontsize=8.2, fontweight='bold', color=header_col, fontfamily='sans-serif', zorder=5)
            ax.text(x + 0.50, content_y, f"{lead}: ", ha='left', va='center',
                    fontsize=8.2, fontweight='bold', color='#0F172A', fontfamily='sans-serif', zorder=5)
            offset_x = 0.50 + (len(lead) + 2) * 0.066
            ax.text(x + offset_x, content_y, body, ha='left', va='center',
                    fontsize=8.0, fontweight='normal', color='#334155', fontfamily='sans-serif', zorder=5)
            content_y -= 0.46

    # -------------------------------------------------------------
    # 3. TOP ROW CARDS (Y = 5.4 to 8.4, Height = 3.0)
    # -------------------------------------------------------------
    # CARD 1: JAMMER (ECM THREAT NODE) - Top Left
    draw_card(
        ax, x=0.8, y=5.4, w=3.6, h=3.0,
        border_col=C_RED_BDR, header_col=C_RED_HDR,
        domain_tag="ADVERSARY ELECTRONIC ATTACK (EA)",
        title="JAMMER (ECM THREAT NODE)",
        subtitle="Hostile Tactical Interference Generator",
        items=[
            ("Waveforms", "Spot, Multi-Spot, Swept Chirp, Barrage"),
            ("Emission", "Direct RF denial power injection J_k"),
            ("Tactical Intent", "Targeted carrier denial & link suppression"),
            ("Threat Agility", "Fast frequency hopping & cyclic sweep")
        ]
    )

    # CARD 2: CONTESTED RF MEDIUM - Top Center
    draw_card(
        ax, x=5.8, y=5.4, w=4.8, h=3.0,
        border_col=C_SLATE_BDR, header_col=C_SLATE_HDR,
        domain_tag="PHYSICAL ELECTROMAGNETIC CHANNEL",
        title="CONTESTED RF MEDIUM",
        subtitle="Superposed Multi-Channel Propagation Model",
        items=[
            ("Channels", "N Tactical Bands (CH0 to CH_N-1)"),
            ("Noise & Fading", "Thermal AWGN floor & Rayleigh fading g_k"),
            ("Superposition", "Friendly Carrier P_rx,k + Hostile ECM J_k"),
            ("Impairment", "Total Spectral Interference I_k = N0 + J_k")
        ]
    )

    # CARD 3: ES SENSING RECEIVER - Top Right
    draw_card(
        ax, x=12.0, y=5.4, w=4.2, h=3.0,
        border_col=C_BLUE_BDR, header_col=C_BLUE_HDR,
        domain_tag="ELECTRONIC SUPPORT (ES)",
        title="RECEIVER (ES NODE)",
        subtitle="Spectrum Telemetry & Sensing Ingestion",
        items=[
            ("Surveillance", "Wideband channelized energy detection"),
            ("Link Metric", "Instantaneous SINR quality evaluation"),
            ("Tri-State Logic", "Partitions into FREE, DEGRADED, BLOCKED"),
            ("Data Bus Out", "Packages spectral evidence into CRRequest")
        ]
    )

    # -------------------------------------------------------------
    # 4. BOTTOM ROW CARDS (Y = 1.2 to 4.2, Height = 3.0)
    # -------------------------------------------------------------
    # CARD 6: SYSTEM BUS LEGEND - Bottom Left (Aligned with Jammer)
    lx, ly, lw, lh = 0.8, 1.2, 3.6, 3.0
    ax.add_patch(patches.FancyBboxPatch((lx+0.04, ly-0.04), lw, lh, boxstyle='round,pad=0.01,rounding_size=0.14',
                                        facecolor='#E2E8F0', edgecolor='none', zorder=1))
    leg_box = patches.FancyBboxPatch((lx, ly), lw, lh, boxstyle='round,pad=0.01,rounding_size=0.14',
                                     facecolor='#FFFFFF', edgecolor='#94A3B8', linewidth=1.4, zorder=2)
    ax.add_patch(leg_box)
    
    leg_hdr = patches.FancyBboxPatch((lx, ly + lh - 0.48), lw, 0.48, boxstyle='round,pad=0.01,rounding_size=0.14',
                                     facecolor='#334155', edgecolor='#334155', linewidth=1, zorder=3)
    ax.add_patch(leg_hdr)
    ax.add_patch(patches.Rectangle((lx, ly + lh - 0.48), lw, 0.25, facecolor='#334155', edgecolor='#334155', zorder=3))
    ax.text(lx + lw/2, ly + lh - 0.24, "SYSTEM DATA BUS LEGEND", ha='center', va='center',
            fontsize=8.5, fontweight='bold', color='#FFFFFF', fontfamily='sans-serif', zorder=4)

    # Clean 4-bus legend with ample spacing
    leg_entries = [
        ("Hostile ECM Jamming", C_RED_BDR, '--', "Adversary Interference Power J_k"),
        ("Spectral RF Ingestion", C_BLUE_BDR, '-', "Channel Intake (Signal + Jamming)"),
        ("ES Sensing Telemetry", C_BLUE_HDR, '-', "CRRequest Ingestion Telemetry Bus"),
        ("ECCM Control & RF Loop", C_GREEN_HDR, '-', "CRResponse & Friendly Transmission")
    ]
    leg_y = ly + lh - 0.82
    for label, col, ls, desc in leg_entries:
        ax.plot([lx + 0.22, lx + 0.75], [leg_y, leg_y], color=col, lw=2.4, linestyle=ls, zorder=4)
        if ls == '-':
            ax.plot([lx + 0.75], [leg_y], marker='>', markersize=4.5, color=col, zorder=4)
        ax.text(lx + 0.88, leg_y + 0.08, label, fontsize=7.6, fontweight='bold', color='#0F172A', fontfamily='sans-serif', zorder=4)
        ax.text(lx + 0.88, leg_y - 0.12, desc, fontsize=6.8, fontstyle='italic', color='#64748B', fontfamily='sans-serif', zorder=4)
        leg_y -= 0.52

    # CARD 5: TRANSMITTER (ECCM ACTUATOR) - Bottom Center (Aligned with RF Medium)
    draw_card(
        ax, x=5.8, y=1.2, w=4.8, h=3.0,
        border_col=C_GREEN_BDR, header_col=C_GREEN_HDR,
        domain_tag="FRIENDLY ECCM ACTUATOR",
        title="TRANSMITTER (ECCM ACTUATOR)",
        subtitle="Agile Frequency Synthesizer & RF Power Amplifier",
        items=[
            ("RF Synthesizer", "Fast-locking agile Local Oscillator"),
            ("Carrier Hop", "Immediate retune to approved safe carrier"),
            ("Power Control", "Dynamic PA regulation within safe headroom"),
            ("Anti-Jam Hopping", "Real-time execution over clean hop pool")
        ]
    )

    # CARD 4: COGNITIVE DECISION ENGINE - Bottom Right (Aligned with Receiver)
    draw_card(
        ax, x=12.0, y=1.2, w=4.2, h=3.0,
        border_col=C_ENGINE_BDR, header_col=C_ENGINE_HDR,
        domain_tag="COGNITIVE C2 · SAFETY ARBITRATOR",
        title="COGNITIVE DECISION ENGINE & ML",
        subtitle="Transmitter-Attached Neural Policy & Hybrid Safety Gate",
        items=[
            ("Neural Policy", "64x32 MLP Net predicts optimal carrier"),
            ("Softmax Confidence", "Class probability certainty score"),
            ("Hybrid Safety Gate", "Deterministic hard blacklist veto"),
            ("Adaptive Hopping", "Evicts jammed carriers & refills active pool")
        ]
    )

    # -------------------------------------------------------------
    # 5. STRAIGHT, UNBROKEN DATA BUS CONNECTORS
    # Pure orthogonal layout with zero crossing lines
    # -------------------------------------------------------------

    # --- ARROW 1 (TOP LEFT): Jammer -> Contested RF Medium ---
    ax.annotate('', xy=(5.8, 6.9), xytext=(4.4, 6.9),
                arrowprops=dict(arrowstyle='-|>', color=C_RED_BDR, lw=2.5, linestyle='--',
                                mutation_scale=16, shrinkA=0, shrinkB=0), zorder=6)
    ax.text(5.1, 7.35, 'Hostile ECM Jamming', ha='center', va='bottom',
            fontsize=8.0, fontweight='bold', color=C_RED_HDR, fontfamily='sans-serif')
    ax.text(5.1, 7.12, '(Power J_k)', ha='center', va='bottom',
            fontsize=7.0, fontstyle='italic', color=C_RED_HDR, fontfamily='sans-serif')

    # --- ARROW 2 (TOP RIGHT): Contested RF Medium -> ES Receiver ---
    ax.annotate('', xy=(12.0, 6.9), xytext=(10.6, 6.9),
                arrowprops=dict(arrowstyle='-|>', color=C_BLUE_BDR, lw=2.5,
                                mutation_scale=16, shrinkA=0, shrinkB=0), zorder=6)
    ax.text(11.3, 7.35, 'Spectral RF Intake', ha='center', va='bottom',
            fontsize=8.0, fontweight='bold', color=C_BLUE_HDR, fontfamily='sans-serif')
    ax.text(11.3, 7.12, '(Signal + Jamming)', ha='center', va='bottom',
            fontsize=7.0, fontstyle='italic', color=C_BLUE_HDR, fontfamily='sans-serif')

    # --- ARROW 3 (RIGHT VERTICAL): ES Receiver -> Cognitive Decision Engine ---
    ax.annotate('', xy=(14.1, 4.2), xytext=(14.1, 5.4),
                arrowprops=dict(arrowstyle='-|>', color=C_BLUE_HDR, lw=2.5,
                                mutation_scale=16, shrinkA=0, shrinkB=0), zorder=6)
    ax.text(14.3, 4.95, 'CRRequest Telemetry Bus', ha='left', va='center',
            fontsize=8.0, fontweight='bold', color=C_BLUE_HDR, fontfamily='sans-serif')
    ax.text(14.3, 4.65, '[SINR, Channel States, Power]', ha='left', va='center',
            fontsize=7.0, fontstyle='italic', color='#0284C7', fontfamily='sans-serif')

    # --- ARROW 4 (BOTTOM RIGHT): Cognitive Decision Engine -> Transmitter ---
    ax.annotate('', xy=(10.6, 2.7), xytext=(12.0, 2.7),
                arrowprops=dict(arrowstyle='-|>', color=C_GREEN_HDR, lw=2.6,
                                mutation_scale=16, shrinkA=0, shrinkB=0), zorder=6)
    ax.text(11.3, 3.12, 'CRResponse Control Bus', ha='center', va='bottom',
            fontsize=8.0, fontweight='bold', color=C_GREEN_HDR, fontfamily='sans-serif')
    ax.text(11.3, 2.88, '[Action, Carrier, Hop Pool]', ha='center', va='bottom',
            fontsize=7.0, fontstyle='italic', color='#15803D', fontfamily='sans-serif')

    # --- ARROW 5 (CENTER VERTICAL): Transmitter -> Contested RF Medium (Closing the Loop!) ---
    ax.annotate('', xy=(8.2, 5.4), xytext=(8.2, 4.2),
                arrowprops=dict(arrowstyle='-|>', color=C_GREEN_HDR, lw=2.5,
                                mutation_scale=16, shrinkA=0, shrinkB=0), zorder=6)
    ax.text(8.4, 4.95, 'Closed-Loop RF Carrier', ha='left', va='center',
            fontsize=8.0, fontweight='bold', color=C_GREEN_HDR, fontfamily='sans-serif')
    ax.text(8.4, 4.65, 'Radiated Friendly Signal P_tx,k', ha='left', va='center',
            fontsize=7.0, fontstyle='italic', color='#15803D', fontfamily='sans-serif')

    # -------------------------------------------------------------
    # 6. SAVE OUTPUT AT HIGH RESOLUTION
    # -------------------------------------------------------------
    plt.tight_layout()
    plt.savefig(OUT_PATH, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Refined decluttered diagram successfully generated at: {OUT_PATH}")

if __name__ == "__main__":
    create_decluttered_diagram()
