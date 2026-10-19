def display_score(title: str, dk_value: int, opp_value: int):
    text = f"""
    <div style="
        background-color: #FFFFFF;
        border: 2px solid #E5E7EB;
        border-radius: 12px;
        padding: 20px;
        margin: 15px auto 25px auto;
        max-width: 650px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    ">
        <div style="
            font-size: 0.9rem;
            font-weight: 700;
            color: #6B7280;
            letter-spacing: 2px;
            text-transform: uppercase;
            margin-bottom: 8px;
        ">
            {title.upper()}
        </div>
        <div style="
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 30px;
        ">
            <div style="text-align: center;">
                <span style="font-size: 1.4rem; font-weight: 800; color: #DC2626; display: block;">DK</span>
                <span style="font-size: 3.5rem; font-weight: 900; color: #111827; line-height: 1;">{dk_value}</span>
            </div>
            <div style="font-size: 2.5rem; font-weight: 300; color: #9CA3AF; margin-top: 15px;">-</div>
            <div style="text-align: center;">
                <span style="font-size: 1.4rem; font-weight: 800; color: #374151; display: block;">OPP</span>
                <span style="font-size: 3.5rem; font-weight: 900; color: #111827; line-height: 1;">{opp_value}</span>
            </div>
        </div>
    </div>
"""
    return text
