"""Self-contained browser UI for OVERALL PACHINKO (Streamlit iframe)."""
from __future__ import annotations
import json
import streamlit.components.v1 as components

from pachinko import (PITY_SPINS, PITY_PAYOUT, ST_MAX, BASE_COLOR_WEIGHTS, COLOR_HIT_RATES, PAYOUT_WEIGHTS, SPECIAL_EVENT_RATES)
from pachinko_rank import RANK_THRESHOLDS


def render_pachinko(
    overall_values: list[float],
    simulation_distribution: list[dict] | None = None,
    simulation_count: int = 0,
    app_url: str = "https://ensemble-stars-analyzer.streamlit.app/",
) -> None:
    values_json = json.dumps([round(float(v), 3) for v in overall_values], ensure_ascii=True)
    url_json = json.dumps(app_url)
    percentile_data_json = json.dumps(simulation_distribution or [], ensure_ascii=True)
    simulation_count = int(simulation_count or 0)
    rank_tiers_json = json.dumps(RANK_THRESHOLDS)
    rush_payouts_json = json.dumps(PAYOUT_WEIGHTS)
    base_colors_json = json.dumps(BASE_COLOR_WEIGHTS)
    color_hit_rates_json = json.dumps(COLOR_HIT_RATES)
    special_event_rates_json = json.dumps(SPECIAL_EVENT_RATES)
    html = r'''<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>
:root{color-scheme:dark}*{box-sizing:border-box}body{margin:0;background:transparent;color:#f8f4e8;font-family:system-ui,-apple-system,"Segoe UI",sans-serif}.machine{max-width:900px;margin:0 auto;padding:16px;border:1px solid #9d792f;border-radius:22px;background:radial-gradient(ellipse at 50% 0%,#34234e 0,#11101d 45%,#07070d 100%);box-shadow:0 0 35px #8b5cf633}.top{display:flex;justify-content:space-between;gap:10px;align-items:center;flex-wrap:wrap}.brand{font-weight:950;letter-spacing:.12em;color:#f5d77b}.brand-sub{margin-top:3px;color:#b9a9d1;font-size:10px;letter-spacing:.08em}.notes{font-weight:900;color:#ffe7a0}.screen{margin:16px 0;padding:20px 12px;border:2px solid #b18a40;border-radius:18px;text-align:center;background:linear-gradient(145deg,#090912,#21182c);box-shadow:inset 0 0 25px #000}.eyebrow{font-size:12px;letter-spacing:.2em;color:#cbb77e}.number{font-size:clamp(44px,12vw,82px);font-weight:1000;letter-spacing:.08em;color:#fff1bd;text-shadow:0 0 18px #d7a93e}.number .d0{color:#f5f5f5}.number .d1{color:#ff6868}.number .d2{color:#68b7ff}.number .d3{color:#65e0a0}.number .d4{color:#d8a0ff}.number .d5{color:#ff9bce}.number .d6{color:#ffe36d}.number .d7{color:#ffd34f;text-shadow:0 0 18px #ffd34f}.number .d8{color:#70e6e1}.number .d9{color:#ff9d52}.number.blackout{color:#050509!important;text-shadow:none!important;filter:brightness(0)}.number.rainbowFlash{background:linear-gradient(90deg,#ff5c5c,#ffcf5c,#75e58b,#61caff,#a987ff,#ff78d2);background-clip:text;-webkit-background-clip:text;color:transparent!important;text-shadow:0 0 24px #fff8}.digit{display:inline-block}.integerPart{color:#f6f6f6}.decimalPart{color:#ffe17b}.message{min-height:28px;color:#f3d88b;font-weight:800}.stats{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:8px}.stat{padding:12px 6px;border:1px solid #5e4a78;border-radius:12px;background:#171324;text-align:center}.stat small{display:block;color:#b9a9d1;font-size:11px}.stat b{font-size:22px;color:#fff}.holds{display:flex;justify-content:center;gap:10px;margin:14px 0;min-height:52px}#holds:empty{display:none}.holds.white-flash .gem{background:linear-gradient(135deg,#fff,#dcecff,#fff)!important;border-color:#fff!important;box-shadow:0 0 24px #fff!important;animation:whiteBlink .18s ease-in-out 2}.holds.white-flash{filter:brightness(1.6)}@keyframes whiteBlink{50%{opacity:.35;transform:rotate(45deg) scale(.85)}}.gem{width:42px;height:42px;transform:rotate(45deg);border:2px solid #8ca6ff;border-radius:8px;background:linear-gradient(135deg,#1647aa,#6dd8ff);box-shadow:0 0 14px #4e9fff88}.gem.green{background:linear-gradient(135deg,#075e42,#70f1ad);border-color:#a2ffca}.gem.red{background:linear-gradient(135deg,#7c102a,#ff647e);border-color:#ffb1be}.gem.gold{background:linear-gradient(135deg,#8a5b08,#ffe28a);border-color:#fff0b5}.gem.gold{background:linear-gradient(135deg,#8a5b08,#ffe28a);border-color:#fff0b5}.gem.rainbow{background:linear-gradient(135deg,red,orange,yellow,lime,cyan,blue,violet);border-color:white}.gem.upgraded{animation:pulse .7s ease-in-out infinite;border-width:4px}.gem.active{transform:rotate(45deg) scale(1.18);filter:brightness(1.35);box-shadow:0 0 22px #fff7b0}.controls{display:flex;gap:10px;justify-content:center;flex-wrap:wrap}.modeSelect{display:flex;flex-wrap:wrap;justify-content:center;align-items:center;gap:9px;margin:10px auto;color:#e8d8a7;font-size:13px}.modeSelect select{background:#211b2c;color:#fff;border:1px solid #9d792f;border-radius:9px;padding:8px 12px;font-weight:800}

.normalModeSelect{display:flex;flex-wrap:wrap;justify-content:center;align-items:center;gap:9px;margin:8px auto 12px;padding:10px 12px;border:1px solid #476a8e;border-radius:12px;background:linear-gradient(110deg,#101b2b,#171c32);color:#d8eaff;font-size:13px}
.normalModeSelect select{background:#101d32;color:#fff;border:1px solid #5b8ec2;border-radius:9px;padding:8px 12px;font-weight:900;max-width:100%}
.normal-mode-description{flex-basis:100%;text-align:center;color:#b9cce4;font-size:12px;line-height:1.5}
.screen.normal-spin{border-color:#5c83bb;box-shadow:inset 0 0 30px #07172c,0 0 14px #4d8ad455}
.screen.normal-tease{border-color:#4fc9d9;box-shadow:inset 0 0 34px #073747,0 0 20px #4fc9d988;animation:normalTease .72s ease-in-out infinite alternate}
.screen.normal-reach{border-color:#e75b77;box-shadow:inset 0 0 36px #4b1028,0 0 24px #f34e7188}
.screen.normal-hot{background:radial-gradient(ellipse at 50% 48%,#51301a 0,#1a1021 55%,#08080f 100%);border-color:#f3c75d;box-shadow:inset 0 0 42px #9a581d,0 0 28px #f7c85c}
.screen.normal-final{animation:normalFinal .72s ease-in-out infinite alternate}
.normal-message{letter-spacing:.04em;text-shadow:0 0 12px #8acaff88}
@keyframes normalTease{from{filter:brightness(.92)}to{filter:brightness(1.28)}}
@keyframes normalFinal{0%{transform:scale(1);filter:brightness(1)}55%{transform:scale(1.012);filter:brightness(1.5)}100%{transform:scale(1);filter:brightness(1.08)}}
@media(max-width:480px){.normalModeSelect{align-items:stretch}.normalModeSelect label{width:100%;text-align:center}.normalModeSelect select{width:100%}}
.rushModeSelect{display:none;flex-wrap:wrap;justify-content:center;align-items:center;gap:9px;margin:8px auto 12px;padding:10px 12px;border:1px solid #6b4058;border-radius:12px;background:linear-gradient(110deg,#17101f,#251322);color:#f4d5df;font-size:13px}
.rushModeSelect.active{display:flex}.rushModeSelect select{background:#21101d;color:#fff;border:1px solid #b84d68;border-radius:9px;padding:8px 12px;font-weight:900;max-width:100%}
.rush-mode-description{flex-basis:100%;text-align:center;color:#d7b8c7;font-size:12px;line-height:1.5}.rush-trust-note{flex-basis:100%;text-align:center;color:#ffe5a3;font-size:12px;line-height:1.5}.rush-trust-note b{font-size:16px;color:#ff829e;text-shadow:0 0 10px #ff416c}
.screen{position:relative;overflow:hidden;isolation:isolate}
.screen>*{position:relative;z-index:2}
.screen.rush-shadow{background:radial-gradient(ellipse at 50% 42%,#2c0712 0,#10070e 38%,#05050a 78%);border-color:#a72e4c;box-shadow:inset 0 0 50px #000,0 0 28px #d21f4f66}
.screen.rush-shadow:before{content:"";position:absolute;z-index:1;left:50%;top:34%;width:min(76%,460px);height:104px;transform:translate(-50%,-50%);background:radial-gradient(ellipse at 24% 50%,#fff 0 2%,#ff183e 3% 9%,#ff183eaa 10% 17%,transparent 30%),radial-gradient(ellipse at 76% 50%,#fff 0 2%,#ff183e 3% 9%,#ff183eaa 10% 17%,transparent 30%);filter:blur(1px) drop-shadow(0 0 14px #ff123f);animation:shadowEyes .75s ease-in-out infinite alternate}
@keyframes shadowEyes{from{opacity:.18;filter:blur(7px)}to{opacity:1;filter:blur(1px) drop-shadow(0 0 16px #ff174d)}}
.screen.rush-lunge{animation:rushLunge .42s cubic-bezier(.2,.8,.2,1)}
@keyframes rushLunge{0%{transform:scale(1);filter:brightness(.5)}45%{transform:scale(1.035);filter:brightness(2.1)}100%{transform:scale(1);filter:brightness(1.2)}}
.screen.rush-impact{animation:rushImpact .55s ease-out}
.screen.payout-300{border-color:#57aaff;box-shadow:0 0 18px #57aaff88,inset 0 0 26px #123d70}
.screen.payout-1500{border-color:#f5d77b;box-shadow:0 0 24px #f5d77b99,inset 0 0 30px #6c4d16}
.screen.payout-3000{border-color:#ff78c8;box-shadow:0 0 28px #ff4bba,inset 0 0 34px #6d1b57}
.screen.payout-4500{border-color:#ff526b;box-shadow:0 0 34px #ff526b,inset 0 0 40px #6b102a}
.screen.payout-6000{border-color:#fff;box-shadow:0 0 48px #ff4bd8,inset 0 0 48px #5d2875;animation:premiumJackpot .65s ease-in-out infinite alternate}

@keyframes rushImpact{0%{transform:translateX(0);filter:brightness(1)}12%{transform:translateX(-7px);filter:brightness(2)}24%{transform:translateX(7px)}36%{transform:translateX(-4px)}52%{transform:translateX(4px);filter:brightness(1.6)}100%{transform:translateX(0);filter:brightness(1)}}
body[data-chain="4-7"] .screen{box-shadow:0 0 22px #ff9b52,inset 0 0 28px #7a2b22}
body[data-chain="8-11"] .screen{box-shadow:0 0 32px #ff526b,inset 0 0 36px #8a173c}
body[data-chain="12-plus"] .screen{border-color:#ffcf5c;box-shadow:0 0 42px #ff4bd8,inset 0 0 45px #56205f;animation:chainPulse 1.25s ease-in-out infinite alternate}
@keyframes chainPulse{to{filter:brightness(1.25);box-shadow:0 0 55px #ff4bd8,inset 0 0 55px #56205f}}
.rush-chain-badge{display:inline-block;margin-left:7px;padding:3px 8px;border:1px solid #d9b83e;border-radius:999px;color:#ffe69a;font-size:11px;vertical-align:middle}
@media(max-width:480px){.rushModeSelect{align-items:stretch}.rushModeSelect label{width:100%;text-align:center}.rushModeSelect select{width:100%}}
.award-list{display:flex;flex-wrap:wrap;gap:6px;margin-top:8px}.achievement-toast{display:none;position:sticky;top:6px;z-index:20;margin:8px auto;padding:9px 14px;width:max-content;max-width:95%;border:1px solid #f5d77b;border-radius:12px;background:#35243e;color:#ffe69a;font-weight:900;text-align:center;box-shadow:0 0 18px #ffcf5c66}.achievement-toast.show{display:block}.award-chip{display:inline-block;padding:5px 9px;border:1px solid #d9b83e;border-radius:999px;color:#ffe69a;background:#30233b;font-size:12px;font-weight:900}.rush-phase{font-size:12px;color:#ffe17b;font-weight:900;letter-spacing:.08em}.btn{border:0;border-radius:14px;padding:14px 22px;font-weight:950;font-size:16px;cursor:pointer;color:#18101c;background:linear-gradient(135deg,#f9df8b,#b77b26);box-shadow:0 5px 0 #754d1c;touch-action:none}.btn:disabled{opacity:.35;cursor:not-allowed}.btn,.gem,.holds,.stat{-webkit-user-select:none;user-select:none;-webkit-touch-callout:none}.btn{touch-action:manipulation}.holdButton{touch-action:none;-webkit-user-select:none;user-select:none;-webkit-touch-callout:none}.volumeRow{display:flex;flex-wrap:wrap;align-items:center;justify-content:center;gap:10px;margin:12px auto;color:#c9c2d5;font-size:12px}.volumeRow span:last-child{flex-basis:100%;text-align:center}.volumeRow input{width:140px;accent-color:#e6bd43}.btn.secondary{background:linear-gradient(135deg,#b4b4ff,#5d5ab2);color:#0e0d25;box-shadow:0 5px 0 #34316f}.hint{text-align:center;color:#a9a1b8;font-size:12px;line-height:1.6}.result{margin-top:16px;padding:16px;border:1px solid #a98746;border-radius:16px;background:#15111e}.spec{margin:14px 0;padding:14px;border:1px solid #5c4b70;border-radius:14px;background:#151323}.spec h3{margin:0 0 8px;color:#f5d77b}.specgrid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}@media(max-width:650px){.machine{padding:10px;border-radius:16px}.stats{grid-template-columns:repeat(2,minmax(0,1fr))}.rank-next{margin-left:0;flex-basis:100%}.specgrid{grid-template-columns:1fr}.screen{margin:10px 0;padding:18px 8px}.stats{grid-template-columns:repeat(2,minmax(0,1fr));gap:6px}.stat{padding:9px 4px}.rank-progress{margin:8px 0 12px}.rank-progress-top{gap:7px}.rank-next{margin-left:0;flex-basis:100%;font-size:11px}.rushModeSelect,.normalModeSelect{margin:8px 0;padding:10px}.rushModeSelect select,.normalModeSelect select{width:100%}.rushModeSelect label,.normalModeSelect label{width:100%;text-align:center}.rush-trust-note{font-size:11px}.volumeRow{margin:8px auto}.holds{gap:7px;min-height:42px;margin:10px 0}.gem{width:34px;height:34px}.btn{padding:15px 24px;font-size:17px}.controls{margin:8px 0}.pieWrap{justify-content:center}.time-pie{background:conic-gradient(#a987ff 0 100%)!important;position:relative;border:0}\n.miniPie{width:100px;height:100px}}.spec table{width:100%;border-collapse:collapse;font-size:13px}.spec td,.spec th{padding:5px;border-bottom:1px solid #4b4059;text-align:left}.initial-pie-layout{display:flex;align-items:center;gap:14px;flex-wrap:wrap;margin:10px 0}.initial-pie{width:clamp(130px,22vw,190px);height:clamp(130px,22vw,190px);border:5px solid #29243a;flex:none}.initial-legend{display:grid;gap:8px;min-width:220px;flex:1}.initial-legend div{display:grid;grid-template-columns:12px 1fr auto;align-items:center;gap:7px;font-size:13px}.initial-legend i{width:11px;height:11px;border-radius:50%;display:block}.initial-legend b{font-variant-numeric:tabular-nums}.initial-legend .pity-legend{color:#ff8be8;font-weight:900}.expected-value-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:9px;margin:14px 0}.expected-value-grid>div{padding:12px;border:1px solid #5c4b70;border-radius:12px;background:#211b2c}.expected-value-grid small{display:block;color:#b9a9d1;font-size:12px;margin-bottom:5px}.expected-value-grid b{font-size:clamp(16px,2vw,22px);color:#ffe08a;font-variant-numeric:tabular-nums}.expected-value-grid .expected-total{border-color:#b18a40;background:linear-gradient(120deg,#30233b,#211b2c)}.expected-value-grid .expected-total b{color:#ffdf78}@media(max-width:650px){.initial-pie-layout{justify-content:center}.initial-legend{min-width:100%}.expected-value-grid{grid-template-columns:1fr}}.spec .ev{color:#ffe08a;font-weight:900}.resultHero{text-align:center;padding:12px;border:1px solid #b28b42;border-radius:12px;background:linear-gradient(110deg,#24152f,#101b3b,#32152c)}.resultHero b{font-size:clamp(28px,6vw,44px);color:#ffe17b}.heroLine{display:flex;align-items:center;justify-content:center;gap:24px;flex-wrap:wrap}.heroLine strong{font-size:clamp(34px,7vw,58px)}.rank-rainbow{background:linear-gradient(90deg,#ff5c5c,#ffcf5c,#75e58b,#61caff,#a987ff,#ff78d2);background-clip:text;-webkit-background-clip:text;color:transparent}.rank-gold{color:#f5c84b}.rank-pink{color:#ff91bd}.rank-purple{color:#bd83ee}.rank-red{color:#f05b70}.rank-purple{color:#bd83ee}.rank-blue{color:#57aaff}.rank-green{color:#5bd18b}.rank-yellow{color:#f0d34f}.rank-orange{color:#f29b4b}.rank-cyan{color:#58c9dc}.rank-gray{color:#a5a5a5}.rank-silver{color:#d4d8e0}.rank-darkgray{color:#777}
/* 4:3 editorial result card based on the supplied reference */
.result{width:100%;max-width:1100px;margin:18px auto 0;padding:0;border:0;border-radius:0;background:transparent;box-shadow:none;overflow:visible}#resultGrid{display:block;min-height:0;width:100%;padding:clamp(12px,2vw,24px);border:5px solid #d6a832;border-radius:0;background:radial-gradient(ellipse at 50% 35%,#21152d 0,#100d1b 70%,#080711 100%);box-shadow:0 0 0 3px #513a16 inset;overflow:visible}
.result h2{font-size:clamp(18px,2.2vw,30px);letter-spacing:.04em;border-bottom:3px solid #e8c64f;padding:8px 0 9px;margin:8px 0 12px;color:#f6d65d}
.resultCardHead{display:grid;grid-template-columns:1.2fr .8fr;gap:10px;margin-bottom:10px}
.rc-panel{border:3px solid #d9b83e;border-radius:17px;padding:12px 15px;background:#151020;min-width:0}
.rc-title{font-weight:900;color:#f5d65d;border-bottom:2px solid currentColor;padding-bottom:6px;margin-bottom:8px;font-size:clamp(13px,1.5vw,20px)}
.rc-total{font-size:clamp(30px,5vw,66px);font-weight:1000;line-height:1.08;white-space:nowrap}.rc-total small{font-size:.32em;color:#fff}
.rc-rank{text-align:center;font-size:clamp(36px,6vw,76px);font-weight:1000;line-height:1.05}
.rc-sub{font-size:clamp(10px,1.2vw,15px);text-align:center;margin-top:4px}
.rc-body{display:grid;grid-template-columns:1fr 1fr 1.18fr;gap:10px}
.rc-pink{border-color:#e66ab1}.rc-pink .rc-title{color:#f18bc8}.rc-cyan{border-color:#54d6e4}.rc-cyan .rc-title{color:#71e8ee}.rc-gold{border-color:#d9b83e}.rc-rows{display:grid;gap:0}.rc-row{display:flex;justify-content:space-between;gap:8px;padding:7px 0;border-bottom:1px solid #65556e;font-size:clamp(10px,1.15vw,15px)}.rc-row b{text-align:right;white-space:normal;overflow-wrap:anywhere;min-width:0}.rc-average{margin-top:10px;padding:8px;border:2px solid #d9b83e;border-radius:12px;text-align:center;color:#f5d65d;font-weight:900}.rc-average strong{display:block;color:#fff;font-size:clamp(17px,2vw,25px)}
.rc-piearea{display:flex;align-items:center;gap:10px}.rc-piewrap{position:relative;width:150px;height:150px;flex:none}.rc-pie{position:absolute;left:25px;top:25px;width:100px;height:100px;border-radius:50%;border:2px solid #f4e5bd}.rc-pie-labels{position:absolute;inset:0;width:150px;height:150px;overflow:visible;pointer-events:none}.rc-pie-labels text{font-weight:900;fill:#fff;text-anchor:middle;paint-order:stroke;stroke:#21172b;stroke-width:2.5px;stroke-linejoin:round;font-size:10px}.rc-legend{display:grid;gap:6px;font-size:clamp(9px,1.05vw,14px)}.rc-legend div{display:flex;align-items:center;gap:6px}.rc-dot{width:10px;height:10px;flex:none;border-radius:2px}.rc-footer{margin-top:10px;border:3px solid #d9b83e;border-radius:16px;padding:10px 14px;min-height:70px}.rc-footer .rc-title{margin-bottom:5px}.rc-brand{position:relative;text-align:center;margin-top:clamp(20px,2.6vw,43px);padding-right:90px;color:#f6e4a6;font-weight:900;font-size:clamp(13px,1.6vw,20px)}.rc-brand small{display:block;font-weight:400;font-size:.75em}
@media(max-width:650px){#resultGrid{min-height:0;padding:10px;border-width:3px;overflow:visible}.resultCardHead{grid-template-columns:1fr}.rc-body{grid-template-columns:minmax(0,1fr)}.rc-body .rc-payout{grid-column:auto}.rc-piearea{justify-content:flex-start}.rc-pie{width:100px}.rc-legend{font-size:11px}.rc-brand{padding-right:72px;margin-top:16px}.rc-row{font-size:12px}}
.pieWrap{display:flex;align-items:center;gap:18px;flex-wrap:wrap;padding:12px}.pie{width:150px;height:150px;border-radius:50%;flex:none}.miniPie{width:112px;height:112px;border-radius:50%;margin:10px auto;border:5px solid #29243a}.time-pie{background:conic-gradient(#a987ff 0 100%)!important;position:relative;border:0}.legend{display:grid;gap:7px;font-size:13px}.legend i{display:inline-block;width:11px;height:11px;border-radius:50%;margin-right:7px}.item.wide{grid-column:1/-1}.rankline{color:#79dcff;font-weight:900;font-size:18px}.award300{color:#75c7ff!important}.award1500{color:#ffe17b!important}.awardRainbow{background:linear-gradient(90deg,#ff5c5c,#ffcf5c,#75e58b,#61caff,#a987ff,#ff78d2);background-clip:text;-webkit-background-clip:text;color:transparent!important;font-weight:1000}.result h2{margin:18px 0 12px;color:#f4d782}.rc-card-brand{font-size:clamp(20px,3vw,28px);font-weight:1000;letter-spacing:.08em;color:#f5d77b;margin:4px 0 12px;text-align:left}.grid{display:grid;grid-template-columns:1fr 1fr;gap:8px}#resultGrid{display:block}.item{padding:9px;background:#211b2c;border-radius:9px}.item small{display:block;color:#b9a9d1}.actions{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px}.actions .btn{flex:1}.save-preview{margin:14px auto 0;text-align:center;padding:12px;border:1px solid #6c5b7d;border-radius:12px;background:#100d1b}.save-preview p{font-size:13px;color:#f5e7ae}.save-preview img{display:block;width:100%;max-width:800px;height:auto;margin:0 auto;-webkit-touch-callout:default;user-select:none;-webkit-user-select:none;touch-action:pan-y}.save-preview.hidden{display:none!important}.hidden{display:none!important}.pulse{animation:pulse .6s ease}@keyframes pulse{50%{transform:scale(1.12);filter:brightness(1.8)}}.rank-progress{margin:10px 0 14px;padding:10px 13px;border:1px solid #92763d;border-radius:12px;background:linear-gradient(110deg,#21172d,#171020);color:#f8e6a4}.rank-progress-top{display:flex;align-items:center;gap:10px;flex-wrap:wrap;font-size:12px}.rank-progress-top b{font-size:22px;color:#ffe17b}.rank-progress-top b.rank-rainbow{background:linear-gradient(90deg,#ff5c5c,#ffcf5c,#75e58b,#61caff,#a987ff,#ff78d2);background-clip:text;-webkit-background-clip:text;color:transparent!important}.rank-progress-top b.rank-gold{color:#f5c84b!important}.rank-progress-top b.rank-red{color:#f05b70!important}.rank-progress-top b.rank-blue{color:#57aaff!important}.rank-progress-top b.rank-green{color:#5bd18b!important}.rank-progress-top b.rank-pink{color:#ff91bd!important}.rank-progress-top b.rank-purple{color:#bd83ee!important}.rank-progress-top b.rank-gray{color:#a5a5a5!important}.rank-next{margin-left:auto;color:#d8cee8}.rank-progress-track{height:7px;margin-top:8px;background:#42364b;border-radius:8px;overflow:hidden}.rank-progress-track i{display:block;height:100%;width:0;background:linear-gradient(90deg,#e6bd43,#ff77b7,#7bcbff);transition:width .35s ease}.rank-progress-foot{margin-top:5px;text-align:right;font-size:10px;color:#b9a9d1}.manual-intro{font-size:13px;line-height:1.8;color:#d8cee8;padding:8px 2px}.manual-nav{display:grid;grid-template-columns:repeat(auto-fit,minmax(145px,1fr));gap:7px;margin:10px 0 14px}.manual-nav a{display:block;padding:9px;border:1px solid #67557d;border-radius:9px;color:#f5d77b;text-decoration:none;font-size:12px;font-weight:800;background:#171020}.manual-chapter{margin:8px 0;border:1px solid #67557d;border-radius:10px;padding:9px;background:#171020;scroll-margin-top:12px}.manual-chapter summary{color:#f4d782;font-weight:900}.manual-chapter p{font-size:13px;line-height:1.85;color:#e2dbea}.manual-chapter table{width:100%;border-collapse:collapse;font-size:12px}.manual-chapter th,.manual-chapter td{padding:7px;border-bottom:1px solid #514364;text-align:left}.manual-chapter th{color:#f5d77b}.guide{margin:12px 0;border:1px solid #514364;border-radius:12px;padding:10px}.guide summary{cursor:pointer;color:#e8d8a7;font-weight:800}.guide p{font-size:13px;color:#c9c2d5;line-height:1.7}.guide table{width:100%;border-collapse:collapse;font-size:12px}.guide th,.guide td{padding:6px 8px;border-bottom:1px solid #514364;text-align:left}.guide th{color:#f5d77b}.rank-guide-grid{max-width:760px}.simulation-note{font-size:11px;color:#b9a9d1}.rush{color:#9bdcff}.jackpot{color:#fff3a0;text-shadow:0 0 18px #ffe65c}.award3000,.award4500,.award6000{background:linear-gradient(90deg,#ff5c5c,#ffcf5c,#75e58b,#61caff,#a987ff,#ff78d2);background-clip:text;-webkit-background-clip:text;color:transparent!important;font-weight:1000}.award1500{color:#f5c84b!important}.award300{color:#48a9ff!important}.awardSilver{color:#c5cbd4!important}.burst{position:relative;isolation:isolate}.burst:before{content:"✦ ✧ ✦ ✧ ✦";position:absolute;inset:-30px;display:grid;place-items:center;font-size:clamp(35px,9vw,90px);letter-spacing:.18em;color:#fff;text-shadow:0 0 12px #fff,0 0 28px #ff4bdb,0 0 48px #53eaff;animation:burst .95s ease-out both;pointer-events:none;z-index:3}@keyframes burst{0%{opacity:0;transform:scale(.25) rotate(-20deg)}35%{opacity:1;transform:scale(1.2) rotate(8deg)}100%{opacity:0;transform:scale(1.65) rotate(25deg)}}body[data-mode="simple"] .burst:before{display:none}body[data-mode="premium"] .burst:before{font-size:clamp(50px,12vw,120px);text-shadow:0 0 18px #fff,0 0 38px #ff4bdb,0 0 65px #53eaff}
.mode-description{flex-basis:100%;font-size:11px;line-height:1.5;color:#c9c2d5;margin-top:2px;max-width:720px;text-align:center}
body[data-mode="simple"] .screen{box-shadow:none}
body[data-mode="simple"] .number.pulse{animation-duration:.45s}
.last-ten-jackpot{box-shadow:0 0 0 5px #fff,inset 0 0 70px #ffdb70,0 0 65px #ff4bd8!important;animation:lastTenJackpot .48s ease-in-out 3 alternate}@keyframes lastTenJackpot{to{filter:brightness(1.75);transform:scale(1.018)}}.pityFlash{color:#ff8be8!important;text-shadow:0 0 18px #ff4bd8!important;animation:pulse .8s ease-in-out infinite}.pity-burst:before{content:"✧ TIME MODE ✧";color:#ff8be8;text-shadow:0 0 18px #ff4bd8,0 0 36px #a987ff;animation:burst 1.1s ease-out both}.jackpot-simple .number.rainbowFlash{filter:drop-shadow(0 0 10px #fff)}.jackpot-balance{background:linear-gradient(145deg,#090912,#30203d)!important;box-shadow:0 0 24px #f5d77b,inset 0 0 28px #8b5cf6!important}.jackpot-premium{background:radial-gradient(ellipse at 50% 50%,#5c2875,#11101d 72%)!important;box-shadow:0 0 38px #ff4bd8,inset 0 0 36px #53eaff!important;animation:premiumJackpot 1.1s ease-in-out infinite alternate}@keyframes premiumJackpot{to{filter:brightness(1.45);transform:scale(1.012)}}body[data-mode="premium"] .screen{box-shadow:0 0 22px #b66cff, inset 0 0 20px #4e2a76}
body[data-mode="premium"] .jackpot{ text-shadow:0 0 8px #fff,0 0 18px #ff4bdb,0 0 30px #53eaff}
body[data-mode="premium"] .number.rainbowFlash{filter:drop-shadow(0 0 12px #ff8be8)}
body[data-phase="chance-zone"] .screen{border-color:#f1c75b}
body[data-phase="high-chance"] .screen{border-color:#ff8a55;box-shadow:0 0 16px #ff8a55}
body[data-phase="count-down"] .screen{border-color:#ff526b;box-shadow:0 0 20px #ff526b}
body[data-phase="final-chance"] .screen{border:3px solid #ff2e85;box-shadow:0 0 28px #ff2e85}


/* fit the complete reference card inside the embedded 900px game frame */
.rc-title{font-size:16px;line-height:1.25}.rc-total{font-size:46px}.rc-rank{font-size:46px;white-space:nowrap}.rc-sub{font-size:12px}.rc-panel{padding:9px 11px}.rc-body{gap:8px}.rc-row{font-size:12px;padding:6px 0;min-width:0;overflow-wrap:anywhere}.rc-row b{font-variant-numeric:tabular-nums;overflow-wrap:anywhere}.rc-total,.rc-rank{overflow-wrap:anywhere;white-space:normal;min-width:0}.rc-piearea{gap:8px}.rc-pie{width:100px}.rc-legend{font-size:11px;gap:5px}.rc-dot{width:9px;height:9px}.rc-average{padding:6px;margin-top:7px}.rc-average strong{font-size:19px}.rc-footer{min-height:62px;padding:8px 12px;font-size:13px}.rc-brand{margin-top:12px;font-size:16px}
@media(max-width:650px){.rc-title{font-size:14px}.rc-total{font-size:38px}.rc-rank{font-size:42px}.rc-body{grid-template-columns:minmax(0,1fr)}.rc-body .rc-payout{grid-column:auto}.rc-pie{width:100px}.rc-legend{font-size:11px}}

.eyebrow.time-mode{color:#7ceaff;text-shadow:0 0 12px #28bfff}.screen.time-entry,.screen.time-spin{border-color:#61dfff!important;background:radial-gradient(ellipse at center,#17466a 0,#101b3b 55%,#070b18 100%)!important;box-shadow:0 0 30px #36cfff,inset 0 0 45px #1a9bd0!important}.screen.time-spin{animation:timePulse .65s ease-in-out infinite alternate}@keyframes timePulse{to{filter:brightness(1.45);transform:scale(1.012)}}.pity-countdown{margin:10px auto 14px;max-width:620px;padding:10px 14px;border:1px solid #e4b84b;border-radius:12px;background:linear-gradient(100deg,#24172d,#382018);color:#ffe9a0;font-weight:900;text-align:center;box-shadow:0 0 18px #f0b84b55}.pity-countdown.urgent{border-color:#ff587a;color:#fff;box-shadow:0 0 24px #ff315f88;animation:pityPulse .65s ease-in-out infinite alternate}.pity-track{height:5px;margin-top:8px;border-radius:8px;background:#45364b;overflow:hidden}.pity-track i{display:block;height:100%;width:0;background:linear-gradient(90deg,#f0b84b,#ff5b7c);transition:width .25s ease}@keyframes pityPulse{to{filter:brightness(1.45);transform:scale(1.01)}}
.screen.rush-one-push{background:radial-gradient(circle at 50% 50%,#2b2444 0,#090810 48%,#000 100%);border-color:#a987ff;box-shadow:inset 0 0 55px #000,0 0 24px #a987ff66}.screen.rush-special-win{animation:rushWinRainbow .85s ease-in-out 2;border-color:#fff;background:linear-gradient(120deg,#ff4e65,#ffca4e,#65e58e,#54caff,#a67bff,#ff70c9)!important;box-shadow:0 0 42px #fff,inset 0 0 36px #fff!important}.screen.rush-special-miss{filter:brightness(.78);border-color:#806d87}.screen.rush-impact{animation:rushImpact .42s ease-in-out 2}.screen.rush-shadow.rush-lunge:after{content:"";position:absolute;inset:0;z-index:1;background:radial-gradient(ellipse at center,transparent 15%,#000 75%);animation:shadowLunge .42s ease-out both;pointer-events:none}@keyframes rushWinRainbow{0%{filter:brightness(1);transform:scale(1)}45%{filter:brightness(1.8);transform:scale(1.025)}100%{filter:brightness(1.1);transform:scale(1)}}@keyframes shadowLunge{from{opacity:0;transform:scale(1.5)}to{opacity:1;transform:scale(.8)}}
body[data-phase="chance-zone"] .screen{box-shadow:0 0 18px #f1c75b,inset 0 0 22px #8a5d1a}body[data-phase="high-chance"] .screen{box-shadow:0 0 28px #ff8a55,inset 0 0 28px #8c2b20;animation:normalFinal .9s ease-in-out infinite alternate}body[data-phase="count-down"] .screen{box-shadow:0 0 34px #ff526b,inset 0 0 34px #a51d45;animation:normalFinal .55s ease-in-out infinite alternate}body[data-phase="final-chance"] .screen{border:3px solid #fff;box-shadow:0 0 40px #ff2e85,0 0 65px #fff,inset 0 0 35px #ff2e85;animation:normalFinal .35s ease-in-out infinite alternate}
.rc-footer{display:flex;align-items:center;min-height:56px;border-bottom:3px solid #d9b83e;overflow-wrap:anywhere}.rc-date{width:100%;text-align:left;font-size:clamp(11px,1.1vw,15px);line-height:1.5;overflow-wrap:anywhere}.modeSelect,.mode-description{display:none!important}
</style></head><body><div class="machine">
<div id="achievementToast" class="achievement-toast" role="status" aria-live="polite"></div><div class="top"><div><div class="brand">OVERALL PACHINKO</div></div><div class="notes">NOTES <span id="notes">0</span></div></div>
<div class="screen" id="screen"><div class="eyebrow" id="mode">NORMAL MODE</div><div class="number" id="number">---.---</div><div class="message" id="message">STARTを押して抽選</div></div>
<div class="holds" id="holds"></div><div class="controls"><button class="btn" id="start">▶ START</button><button class="btn secondary holdButton hidden" id="hold" type="button" aria-label="HOLD保留を長押しで追加">◆ HOLD 長押し</button></div>
<div class="hint" id="hint">通常モード：1回のタップで1回抽選</div><div id="pityCountdown" class="pity-countdown hidden"><span id="pityCountdownText"></span><div class="pity-track"><i id="pityCountdownBar"></i></div></div><div class="stats"><div class="stat"><small>ST</small><b id="st">—</b></div><div class="stat"><small>HOLD</small><b id="holdCount">0 / 5</b></div><div class="stat"><small>RUSH連チャン</small><b id="combo">0回</b></div><div class="stat"><small>初当たり回転数</small><b id="initialSpins">0回</b></div><div class="stat"><small>RUSH消化回転数</small><b id="rushSpinCount">0回</b></div></div>
<div class="volumeRow"><label for="volume">音量</label><input id="volume" type="range" min="0" max="100" value="55"><span id="volumeValue">55%</span><span>音量設定を調整してお楽しみください。</span></div>
<div class="normalModeSelect" id="normalModePanel"><label for="normalMode">通常時演出</label><select id="normalMode"><option value="STANDARD" selected>STANDARD ／ 王道バランス</option><option value="FORESHADOW">FORESHADOW ／ 先読み重視</option><option value="QUICK">QUICK ／ テンポ重視</option></select><div class="normal-mode-description" id="normalModeDescription">STANDARD：演出をバランスよく楽しむ王道モード。</div></div><div class="rushModeSelect" id="rushModePanel"><label for="rushMode">RUSH演出モード</label><select id="rushMode"><option value="STANDARD" selected>STANDARD ／ 王道バランス</option><option value="SHADOW">SHADOW VISITOR ／ 暗闇・襲来告知</option><option value="IMPACT">IMPACT ／ 閃光・衝撃告知</option><option value="ONE_PUSH">ONE PUSH ／ 任意タイミング解放</option></select><div class="rush-mode-description" id="rushModeDescription">STANDARD：演出をバランスよく楽しむ王道モード。</div><div class="rush-trust-note">SHADOW VISITOR・IMPACT・ONE PUSHの専用演出（煽りを含む）の大当たり信頼度：<b>40%</b></div></div>
<div class="rank-progress" id="rankProgress"><div class="rank-progress-top"><span>現在のRANK</span><b id="currentRank">F</b><span class="rank-next" id="nextRankText">次のRANKまで 1,500 NOTES</span></div><div class="rank-progress-track"><i id="rankProgressBar"></i></div><div class="rank-progress-foot" id="rankProgressFoot">300 / 1,500 NOTES</div></div>
<details class="guide"><summary>スペック・特図・保留信頼度</summary><div class="spec"><h3>SPECIFICATION / スペック・出玉振り分け</h3><div class="specgrid">
<div class="initial-spec"><b>特図1：通常時</b><div class="initial-pie-layout"><div class="miniPie initial-pie" style="background:conic-gradient(#399cff 0 26.923%,#e6bd43 26.923% 82.692%,#e85c86 82.692% 98.077%,#a987ff 98.077% 100%)"></div><div class="initial-legend">
<div><i style="background:#399cff"></i><span>300 NOTES</span><b>約26.9%</b></div>
<div><i style="background:#e6bd43"></i><span>1,500 NOTES</span><b>約55.8%</b></div>
<div><i style="background:#e85c86"></i><span>3,000 NOTES</span><b>約15.4%</b></div>
<div><i style="background:#a987ff"></i><span>4,500 NOTES</span><b>約1.9%</b></div>

</div></div>
<p>通常大当たり確率：52/1,799（約1/34.6）。150回転連続未当たりで時短へ移行します。</p>
<p class="simulation-note">円グラフは通常時の大当たり52件のみを対象とし、時短突入・時短大当たりを含みません。</p></div>
<div class="time-spec"><b>特図2：時短</b><div class="initial-pie-layout"><div class="miniPie time-pie" role="img" aria-label="6,000 NOTES 100パーセント"></div><div class="initial-legend"><div><i style="background:#a987ff"></i><span>6,000 NOTES</span><b>100%</b></div></div></div><p>大当たり確率：約1/34.6</p><p>時短回数：131回転</p><p>時短中の大当たり期待度：約97.9％</p><p>大当たり時：ALL 6,000 NOTES＋RUSH確定</p><p>131回転で当たらなければ通常時へ戻ります。</p></div><div><b>特図3：RUSH特図</b><table><tr><td><i style="display:inline-block;width:10px;height:10px;border-radius:50%;background:#399cff;margin-right:6px"></i><span style="color:#48a9ff;font-weight:900">300 NOTES</span></td><td>20%</td></tr><tr><td><i style="display:inline-block;width:10px;height:10px;border-radius:50%;background:#e6bd43;margin-right:6px"></i><span style="color:#f5c84b;font-weight:900">1,500 NOTES</span></td><td>50%</td></tr><tr><td><i style="display:inline-block;width:10px;height:10px;border-radius:50%;background:#e85c86;margin-right:6px"></i><span style="color:#e85c86;font-weight:900">3,000 NOTES</span></td><td>15%</td></tr><tr><td><i style="display:inline-block;width:10px;height:10px;border-radius:50%;background:#ff5c78;margin-right:6px"></i><span style="color:#ff7b8f;font-weight:900">4,500 NOTES</span></td><td>10%</td></tr><tr><td><i style="display:inline-block;width:10px;height:10px;border-radius:50%;background:#a987ff;margin-right:6px"></i><span style="color:#b99cff;font-weight:900">6,000 NOTES</span></td><td>5%</td></tr></table>
<div class="miniPie" style="background:conic-gradient(#399cff 0 20%,#e6bd43 20% 70%,#e85c86 70% 85%,#ff5c78 85% 95%,#a987ff 95% 100%)"></div></div></div>
<div class="expected-value-grid">
<div><small>通常初当たり期待出玉</small><b>1,465 NOTES</b></div>
<div><small>時短突入を含む初当たり期待出玉</small><b>1,520 NOTES</b></div>
<div><small>RUSH獲得期待出玉</small><b>8,511 NOTES</b></div>
<div class="expected-total"><small>総獲得期待出玉（初当たり＋RUSH）</small><b>10,030 NOTES</b></div>
</div>
<p>RUSH大当たり確率 1/73 ／ ST116回転＋残保留最大4個 ／ RUSH継続率 約81% ／ RUSH大当たり1回平均 2,010 NOTES</p>
<p>時短突入確率：約1.23%（通常時150回転連続未当たり）</p>
<div class="hold-trust"><b>保留信頼度・出現率</b><table><tr><th>保留色</th><th>信頼度</th><th>出現率</th></tr><tr><td style="color:#68b7ff;font-weight:900">青</td><td>約0.5%</td><td>90%</td></tr><tr><td style="color:#65e0a0;font-weight:900">緑</td><td>約3%</td><td>9%</></tr><tr><td style="color:#ff647e;font-weight:900">赤</td><td>約60%</td><td>0.9%</></tr><tr><td style="color:#ffe28a;font-weight:900">金</td><td>約85%</td><td>0.09%</></tr><tr><td style="background:linear-gradient(90deg,red,orange,yellow,lime,cyan,blue,violet);background-clip:text;color:transparent;font-weight:900">虹</td><td>100%</td><td>0.01%</></tr></table><p class="simulation-note">※信頼度は保留色ごとの当選率、出現率は昇格後の最終保留色の割合です。</p></div></div></details>
<details class="guide manual-book"><summary>はじめての方へ｜OVERALL PACHINKO 完全ガイド（全8章）</summary>
<div class="manual-intro">パチンコを初めて遊ぶ方にも分かるように、ゲームの目的から抽選の仕組み、保留の見方、RUSH、出玉、RANK、演出用語まで解説します。読みたい章の見出しをタップすると説明が開きます。専門用語はできるだけ日常的な言葉に置き換え、実際のパチンコとの違いも説明しています。</div>

<details class="manual-chapter" id="manual-1"><summary>第1章｜このゲームの目的</summary><p>OVERALL PACHINKOは、パチンコ風ミニゲームです。ゲーム内の単位「NOTES」をできるだけ多く獲得し、最終的な総獲得NOTESとRANKを伸ばすことが目的です。実際の現金や景品を賭けるゲームではありません。</p><p>ゲームは「通常時」→「初当たり」→「RUSH」→「結果」の順に進みます。通常時に大当たりすると出玉を獲得し、必ずRUSHへ突入します。150回転連続で当たらない場合は時短へ移行し、時短中の大当たりで6,000 NOTES＋RUSHを獲得します。RUSH中に当たりを引くと追加NOTESを獲得し、ST116回転が再セットされます。</p></details>
<details class="manual-chapter" id="manual-2"><summary>第2章｜通常時・初当たりの仕組み</summary><p>STARTを押すと、固定されたOVERALLデータ1,799件から1件を重複ありで抽選します。その値の小数点以下3桁が「000」「111」「222」のように同じ数字3つになった場合が初当たりです。該当データは1,799件中52件で、初当たり確率は52/1,799、約1/34.6です。</p><p>通常時の初当たり出玉は、当選した3桁の数字によって決まります。000は1,500 NOTES、先頭数字が7なら4,500 NOTES、先頭数字が偶数なら300 NOTES、奇数なら3,000 NOTESです。固定データ52件の内訳は300 NOTESが14件、1,500 NOTESが29件、3,000 NOTESが8件、4,500 NOTESが1件です。</p><p>抽選結果はSTARTを押した時点で決まり、変動中の光や音などの演出は、その結果を見せるためのものです。演出が弱くても当たる場合があり、強い演出が必ず当たりを意味するわけではありません。</p></details>
<details class="manual-chapter" id="manual-3"><summary>第3章｜遊タイム・時短とは？</summary><p>通常時に150回転連続で大当たりしなかった場合、時短モードへ移行します。突入した時点ではNOTESは付与されません。</p><p>時短は131回転で、大当たり確率は通常時と同じ52/1,799（約1/34.6）です。時短中に大当たりするとALL 6,000 NOTESを獲得し、RUSHへ突入します。131回転で当たらなかった場合は通常時へ戻ります。</p><p>通常時の残り150回転から遊タイムまでのカウントダウンを表示し、残り10回転では表示を強調します。</p></details>
<details class="manual-chapter" id="manual-4"><summary>第4章｜RUSH・ST116回転＋残保留4個</summary><p>RUSHは、大当たり後に連チャン（継続）を狙う特別な遊技状態・モードです。本ゲームではRUSH中の大当たり確率は1/73で、通常時の約1/34.6より低い確率ですが、ST116回転と残保留最大4個の抽選機会によって継続を目指します。STとは、決められた回数だけ大当たり抽選を受けられる仕組みです。</p><p>本ゲームのRUSHはST116回転に加え、ST終了時点で残っている保留を最大4個まで抽選します。つまり、最大で116回転＋残保留4個＝合計120回の抽選機会があります。ST116回転を消化した後は、新しい保留を追加できず、すでに貯まっている保留だけを消化します。残保留がない、または最大4個を消化し終えるとRUSH終了です。</p><p>HOLDボタンを長押しすると0.5秒ごとに保留を追加できます。画面上の保留は最大5個（消化中の1個＋待機中の最大4個）です。ST本体の最後10回転（107～116回転目）と残保留4個を合わせた最大14回転は、消化間隔を通常より長くし、専用BGMを再生します。この14回転中に大当たりすると、専用の豪華な祝福演出が発生します。大当たりを引くとST116回転に再セットされ、未消化の保留は色と抽選結果を保持して次のSTへ持ち越されます。</p><p>STのみの継続期待度は約79.8%、残保留4回を含む最大120回での継続期待度は約81.0%です。これは毎回1/73で独立抽選する前提の理論値です。実際に保留が4個未満なら、その分だけ期待度は低くなります。</p></details>
<details class="manual-chapter" id="manual-5"><summary>第5章｜保留・色・信頼度</summary><p>保留は、これから順番に消化する抽選の待機分です。保留の色は、その保留が当たりである期待度を示す演出上の情報です。色が変わる「保留変化」は、抽選結果そのものを変えるものではありません。</p><table><tr><th>保留色</th><th>当選信頼度</th><th>最終出現割合</th></tr><tr><td>青</td><td>約0.5%</td><td>90%</td></tr><tr><td>緑</td><td>3%</td><td>9%</td></tr><tr><td>赤</td><td>60%</td><td>0.9%</td></tr><tr><td>金</td><td>85%</td><td>0.09%</td></tr><tr><td>虹</td><td>100%</td><td>0.01%</td></tr></table><p>保留は基本色が決まった後、1/50の確率で1段階上に昇格することがあります。表の出現割合は、この昇格後の最終割合です。虹保留は大当たり確定です。色ごとの信頼度を全体で加重平均すると、RUSH大当たり確率1/73になります。</p></details>
<details class="manual-chapter" id="manual-6"><summary>第6章｜演出モード・告知演出</summary><p><b>通常時：</b>STANDARDは演出をバランスよく楽しむ王道モード。FORESHADOWは演出をじっくり楽しむモード。QUICKは変動を短くし、テンポよく楽しむモードです。演出品質はPREMIUM相当に固定されています。</p><p><b>RUSH：</b>STANDARDはバランス型。SHADOW VISITORは暗闇・赤い眼・襲来の気配を使った告知モード。IMPACTは閃光・衝撃・画面振動を使った告知モード。ONE PUSHはボタンを押したタイミングで当落を解放するモードです。</p><p>SHADOW VISITOR・IMPACT・ONE PUSHでは、専用演出（煽りを含む）が発生した場合の大当たり信頼度を40%に設定しています。保留色によって発生しやすさに差を設けていますが、青保留からも発生します。専用演出が発生しない大当たりもあります。</p><p>演出の出現率は、ゲーム抽選とは別の演出専用乱数で決まります。演出モードを変更しても、大当たり確率や出玉振り分けは変化しません。専用告知音はオリジナルの合成音で、大当たり時のみ再生します。</p></details>
<details class="manual-chapter" id="manual-7"><summary>第7章｜出玉・NOTES・RANK</summary><p>RUSH中に大当たりすると、次の割合でNOTESを獲得します。300 NOTES：20%、1,500 NOTES：50%、3,000 NOTES：15%、4,500 NOTES：10%、6,000 NOTES：5%。1回のRUSH大当たりあたりの平均獲得は2,010 NOTESです。</p><p>総獲得NOTESに応じてRANKが決まります。必要NOTESは次のとおりです。</p><table><tr><th>必要NOTES</th><th>RANK</th></tr><tr><td>60,000</td><td>SSS+</td></tr><tr><td>50,400</td><td>SSS</td></tr><tr><td>44,700</td><td>SS+</td></tr><tr><td>40,500</td><td>SS</td></tr><tr><td>36,900</td><td>S+</td></tr><tr><td>33,300</td><td>S</td></tr><tr><td>29,700</td><td>AAA+</td></tr><tr><td>26,400</td><td>AAA</td></tr><tr><td>23,400</td><td>AA+</td></tr><tr><td>20,700</td><td>AA</td></tr><tr><td>18,300</td><td>A+</td></tr><tr><td>15,900</td><td>A</td></tr><tr><td>14,100</td><td>BBB</td></tr><tr><td>12,300</td><td>BB</td></tr><tr><td>9,900</td><td>B</td></tr><tr><td>7,800</td><td>CCC</td></tr><tr><td>5,400</td><td>CC</td></tr><tr><td>3,300</td><td>C</td></tr><tr><td>1,800</td><td>D</td></tr><tr><td>1,500</td><td>E</td></tr><tr><td>300</td><td>F</td></tr></table><p>RANKは総獲得NOTESに応じた固定評価です。リザルトカードの「上位○%」は、100万件のシミュレーション結果のうち、今回の総獲得NOTES以上となった試行の割合です。実際のプレイヤー間ランキングではありません。</p></details>
<details class="manual-chapter" id="manual-8"><summary>第8章｜用語集・よくある質問</summary><p><b>大当たり：</b>ゲーム内の抽選に当選すること。<br><b>初当たり：</b>通常時に最初に引く大当たり。<br><b>RUSH：</b>大当たり確率が1/73になる特別状態。<br><b>ST：</b>決められた回数だけ抽選できる期間。<br><b>残保留：</b>ST終了時にすでに貯まっている、最後に消化する保留。<br><b>保留変化：</b>保留の色が変わり、期待度を示す演出。<br><b>信頼度：</b>その演出や保留が発生したときに大当たりとなる割合。<br><b>出玉振り分け：</b>大当たり時に獲得するNOTESの種類と割合。<br><b>連チャン：</b>大当たりを繰り返してRUSHが続くこと。<br><b>遊タイム：</b>規定回転数まで当たらなかった場合に発動する救済機能。<br><b>回転：</b>1回分の抽選のこと。「1回転」は抽選1回を意味します。<br><b>変動：</b>抽選結果が画面に表示されるまでの演出時間。<br><b>図柄：</b>画面に表示される数字やマーク。揃うと大当たりを表します。<br><b>先読み：</b>対象の保留が消化される前に、色や光などで期待感を示す演出。<br><b>煽り：</b>特定の演出が起こりそうに見せて期待感を高める段階。発生だけで当たりが確定するとは限りません。<br><b>告知：</b>大当たりの可能性や結果を、光・音・画面効果などで知らせること。<br><b>信頼度：</b>その演出が発生した場合に大当たりとなる割合。大当たり確率とは別の数字です。<br><b>出現率：</b>その演出自体が発生する割合。信頼度と混同しないようにします。<br><b>振り分け：</b>当選したときに、どの出玉が選ばれるかの割合。<br><b>継続率：</b>規定回数内に少なくとも1回大当たりする理論上の割合。<br><b>残保留：</b>ST中に追加され、ST本体終了後に消化する待機中の抽選。<br><b>連チャン：</b>大当たり後のRUSHが続き、再び大当たりすること。<br><b>期待出玉：</b>確率や振り分けを長期的に平均した場合の獲得量。1回のプレイで必ず得られる量ではありません。<br><b>NOTES：</b>このミニゲーム内で獲得するポイントの単位。現金や換金価値はありません。<br><b>RANK：</b>獲得NOTESの合計で決まる固定評価。<br><b>STリセット：</b>大当たり後にST回転数を最初から数え直すこと。</p><p><b>Q. 強い演出が出なければ当たりませんか？</b><br>A. いいえ。専用演出がなくても当たる場合があります。</p><p><b>Q. 演出モードで当たりやすさは変わりますか？</b><br>A. 変わりません。演出の見せ方だけが変わります。</p><p><b>Q. ST116回転が終わったらすぐ終了ですか？</b><br>A. いいえ。すでに貯まっている残保留があれば、最大4個まで追加で抽選します。</p><p><b>Q. 121回転目の抽選はありますか？</b><br>A. ありません。1つのST区間で抽選するのは最大120回までです。<br><b>Q. 最終14回転は当たりやすくなりますか？</b><br>A. いいえ。BGMと消化演出を変えて期待感を高めますが、大当たり確率は1/73のままです。</p><p><b>Q. 保留がないと抽選は進みますか？</b><br>A. RUSH中はHOLDボタンを長押しして保留を追加します。ST116回転目を終えると新しい保留は追加できず、すでに貯まっている最大4個だけを消化します。<br><b>Q. 最終14回転の専用BGMはいつ始まりますか？</b><br>A. ST本体の残りが10回転になった時点から始まり、残保留の消化中も継続します。大当たりでSTが再セットされると終了します。<br><b>Q. 次のRANKまでのNOTES表示は何を示しますか？</b><br>A. 現在の総獲得NOTESから次のRANKの必要数まで、あと何NOTES必要かを示します。<br><b>Q. 専用演出が出なかったら外れですか？</b><br>A. いいえ。専用演出が発生しない大当たりもあります。<br><b>Q. 保留色で抽選確率は変わりますか？</b><br>A. 抽選確率を保留色が変えるのではなく、色ごとに当選期待度が異なるように設計しています。全体ではRUSH大当たり確率1/73になるよう調整しています。<br><b>Q. このゲームは実際のパチンコと同じですか？</b><br>A. パチンコの用語や演出構成を参考にしたシミュレーションです。実機の玉の動き、遊技機の認定スペック、店舗での遊技を再現するものではありません。</p></details>
</details>
<details class="guide"><summary>RANK・獲得NOTESの色分けとボーダー</summary><p><b>総獲得NOTES・RUSH獲得NOTESの色：</b>5,000未満は銀色、5,000～9,999は金色、10,000以上は虹色。<br><b>RANKカラー：</b>SSS+ / SSS＝虹色、S系＝金色、A系＝赤色、B系＝青色、C系＝緑色、D＝ピンク、E＝紫色、F＝灰色。</p><div class="rank-guide-grid"><table><tr><th>RANK</th><th>最低獲得NOTES</th></tr>
<tr><td>SSS+</td><td>60,000</td></tr><tr><td>SSS</td><td>50,400</td></tr><tr><td>SS+</td><td>44,700</td></tr><tr><td>SS</td><td>40,500</td></tr><tr><td>S+</td><td>36,900</td></tr><tr><td>S</td><td>33,300</td></tr><tr><td>AAA+</td><td>29,700</td></tr><tr><td>AAA</td><td>26,400</td></tr><tr><td>AA+</td><td>23,400</td></tr><tr><td>AA</td><td>20,700</td></tr><tr><td>A+</td><td>18,300</td></tr><tr><td>A</td><td>15,900</td></tr><tr><td>BBB</td><td>14,100</td></tr><tr><td>BB</td><td>12,300</td></tr><tr><td>B</td><td>9,900</td></tr><tr><td>CCC</td><td>7,800</td></tr><tr><td>CC</td><td>5,400</td></tr><tr><td>C</td><td>3,300</td></tr><tr><td>D</td><td>1,800</td></tr><tr><td>E</td><td>1,500</td></tr><tr><td>F</td><td>300</td></tr></table></div></details>
<div class="result hidden" id="result"><div class="grid" id="resultGrid"></div><div class="actions"><button class="btn" id="save">結果画像を表示・保存</button><button class="btn secondary" id="share">𝕏で共有</button><button class="btn secondary" id="replay">もう一度遊ぶ</button></div><div class="hint">スマートフォンでは表示された画像を長押しして「写真に保存」を選択できます。</div><div id="savePreview" class="save-preview hidden"><p>画像を長押しして「写真に保存」を選択してください。</p><img id="savedResultImage" alt="OVERALL PACHINKO リザルトカード画像"></div></div>
</div>
<script>
const VALUES=__VALUES__,APP_URL=__APPURL__,PERCENTILE_DATA=__PERCENTILE_DATA__,SIMULATION_COUNT=__SIMULATION_COUNT__,RANK_TIERS=__RANK_TIERS__,RUSH_PAYOUTS=__RUSH_PAYOUTS__,PITY_SPINS=__PITY_SPINS__,PITY_PAYOUT=__PITY_PAYOUT__,TIME_SPINS=131,ST_MAX=__ST_MAX__,RESERVE_HOLDS=4,BASE_COLORS=__BASE_COLORS__,COLOR_HIT_RATES=__COLOR_HIT_RATES__,SPECIAL_EVENT_RATES=__SPECIAL_EVENT_RATES__;
const $=id=>document.getElementById(id);let notes=0,started=false,inRush=false,timeMode=false,timeSpins=0,normalStreak=0,ended=false,jackpotAnimating=false,st=0,segmentSpins=0,reserveSpins=0,holds=[],combo=0,maxCombo=0,rushHits=0,rushNotes=0,rushSpins=0,initial=0,initialTriple=null,initialCategory="MISS",initialPayout=0,initialSpins=0,payouts={6000:0,4500:0,3000:0,1500:0,300:0},holdTimer=null,consumeTimer=null,playDate=new Date(),selectedMode="PREMIUM",currentHoldColor="blue",normalMode="STANDARD",rushMode="STANDARD",earnedAchievements=[],rushPayoutsWon=[],rainbowHit=false;
const baseColors=BASE_COLORS;
function weighted(items){let n=Math.floor(Math.random()*items.reduce((a,x)=>a+x[1],0));for(const [v,w] of items){if(n<w)return v;n-=w;}return items[0][0]}
function colorHit(c){return Math.random()<COLOR_HIT_RATES[c]}
function payout(){return weighted(RUSH_PAYOUTS)}
function triple(v){let d=Number(v).toFixed(3).split('.')[1];return /^([0-9])\1\1$/.test(d)?d:null}
function initialAward(t){if(t==='000')return 1500;const d=Number(t[0]);if(d===7)return 4500;return d%2===0?300:3000}
function fmt(n){return Number(n).toLocaleString('ja-JP')}function payoutClass(n){return n>=3000?'awardRainbow':n>=1500?'award1500':'award300'}function rankFor(n){return (RANK_TIERS.find(t=>n>=t[0])||[300,'F'])[1]}function rankColor(r){return ({'SSS+':'rainbow','SSS':'rainbow','SS+':'gold','SS':'gold','S+':'gold','S':'gold','AAA+':'red','AAA':'red','AA+':'red','AA':'red','A+':'red','A':'red','BBB':'blue','BB':'blue','B':'blue','CCC':'green','CC':'green','C':'green','D':'pink','E':'purple','F':'gray'})[r]}function notesColor(n){return n>=10000?'awardRainbow':n>=5000?'award1500':'awardSilver'}function setOverallDisplay(v){const a=Number(v).toFixed(3).split('.');$('number').innerHTML=`<span class="integerPart">${a[0]}.</span><span class="decimalPart">${a[1].split('').map((d)=>`<i class="digit d${d}">${d}</i>`).join('')}</span>`}function setTripleDisplay(v){$('number').innerHTML=String(v).split('').map(d=>`<i class="digit d${d}">${d}</i>`).join('')}
function visualRandom(){const a=new Uint32Array(1);crypto.getRandomValues(a);return a[0]/4294967296;}
function missDigits(){let a=Math.floor(visualRandom()*10),b=Math.floor(visualRandom()*10),c=Math.floor(visualRandom()*10);if(a===b&&b===c)c=(c+1)%10;return ''+a+b+c}
function rushPhase(){if(st===0)return 'RESERVE CHANCE';if(st>=31)return 'RUSH';if(st>=11)return 'CHANCE ZONE';if(st>=6)return 'HIGH CHANCE';if(st>=2)return 'COUNT DOWN';if(st===1)return 'FINAL CHANCE';return 'RUSH END';}
function notifyAchievement(name){if(earnedAchievements.includes(name))return;earnedAchievements.push(name);const toast=$('achievementToast');toast.textContent=`🏆 称号獲得：${earnedAchievements.slice(-2).join(' ／ ')}`;toast.classList.add('show');clearTimeout(toast._hideTimer);toast._hideTimer=setTimeout(()=>toast.classList.remove('show'),2400);}
function evaluateThresholdAchievements(){if(notes>=20000)notifyAchievement('HIGH ROLLER');if(notes>=50000)notifyAchievement('OVERALL KING');}
function normalModeDescription(mode){return ({STANDARD:'STANDARD：演出をバランスよく楽しむ王道モード。',FORESHADOW:'FORESHADOW：演出をじっくり楽しむモード。',QUICK:'QUICK：変動を短くし、テンポよく楽しむモード。'})[mode]||'STANDARD：演出をバランスよく楽しむ王道モード。';}
async function normalSpinPresentation(isHit){
 const screen=$('screen'),message=$('message'),number=$('number'),mode=normalMode;
 const r=visualRandom();
 // 演出段階は演出専用乱数のみ。抽選・保留昇格・出玉抽選には影響しない。
 const tier=isHit?(r<.08?1:r<.40?2:3):(r<.58?0:r<.86?1:r<.97?2:3);
 const pace=mode==='QUICK'?.58:mode==='FORESHADOW'?1.28:1;
 const wait=async(ms)=>sleep(ms*pace);
 screen.classList.remove('normal-tease','normal-reach','normal-hot','normal-final');
 screen.classList.add('normal-spin');message.textContent='';message.className='message normal-message';
 playTone(460,.1,'sine',.035);await wait(mode==='QUICK'?90:150);
 if(tier>=1){screen.classList.add('normal-tease');playTone(590,.16,'triangle',.045);await wait(mode==='FORESHADOW'?360:220);}
 if(tier>=2){screen.classList.remove('normal-tease');screen.classList.add('normal-reach');playTone(780,.18,'sawtooth',.05);await wait(mode==='FORESHADOW'?520:340);}
 if(tier>=3){screen.classList.remove('normal-reach');screen.classList.add('normal-hot','normal-final');playTone(980,.22,'triangle',.065);await wait(mode==='FORESHADOW'?680:440);playTone(1180,.16,'sine',.06);await wait(160);}
 const drum=drumRoll();
 for(let i=0;i<(mode==='QUICK'?8:mode==='FORESHADOW'?16:12);i++){
  number.textContent=(60+visualRandom()*40).toFixed(3);
  await wait(mode==='QUICK'?38:mode==='FORESHADOW'?82:62);
 }
 clearInterval(drum);screen.classList.remove('normal-spin','normal-tease','normal-reach','normal-hot','normal-final');message.className='message';message.textContent='';
}
function rushModeDescription(mode){return ({STANDARD:'STANDARD：演出をバランスよく楽しむ王道モード。',SHADOW:'SHADOW VISITOR：暗闇に潜む気配と襲来の予兆で、当落の瞬間を楽しむ告知モード。',IMPACT:'IMPACT：強烈な閃光と衝撃で、当落の瞬間を楽しむ一発告知モード。',ONE_PUSH:'ONE PUSH：ボタンを押すその瞬間まで結果が分からない、任意タイミング解放モード。'})[mode]||'STANDARD：演出をバランスよく楽しむ王道モード。';}
function achievementList(){const out=[];if(rushHits>=10)out.push('RUSH MASTER');if(rushHits>=20)out.push('RUSH LEGEND');if(initialPayout===6000||rushPayoutsWon.includes(6000))out.push('PREMIUM');if(initialCategory==='TIME MODE')out.push('TIME MODE');if(notes>=50000)out.push('OVERALL KING');if(notes>=20000)out.push('HIGH ROLLER');if(initialSpins===1&&initialTriple)out.push('QUICK START');if(initialSpins===149&&initialTriple)out.push('LAST MOMENT');if(rainbowHit)out.push('RAINBOW');return out;}
function update(){
 $('notes').textContent=fmt(notes);$('notes').className=notesColor(notes);$('initialSpins').textContent=initialSpins+'回';$('st').textContent=inRush?(st>0?st+'回':`残保留 ${holds.length}個`):'—';$('rushSpinCount').textContent=fmt(rushSpins)+'回';$('holdCount').textContent=holds.length>=5?'MAX':holds.length+' / 5';
 const current=RANK_TIERS.find(t=>notes>=t[0])||[300,'F'];const idx=RANK_TIERS.findIndex(t=>t[1]===current[1]);const next=idx>0?RANK_TIERS[idx-1]:null;const first=RANK_TIERS[RANK_TIERS.length-1];$('currentRank').textContent=current[1];$('currentRank').className='rank-'+rankColor(current[1]);if(notes<first[0]){$('nextRankText').textContent=`RANK F まで ${fmt(first[0]-notes)} NOTES`;$('rankProgressBar').style.width=Math.max(0,Math.min(100,notes/first[0]*100))+'%';$('rankProgressFoot').textContent=`${fmt(notes)} / ${fmt(first[0])} NOTES`;}else{$('nextRankText').textContent=next?`次のRANK ${next[1]} まで ${fmt(Math.max(0,next[0]-notes))} NOTES`:'最高RANK到達';const lower=current[0],upper=next?next[0]:current[0];const progress=next?Math.max(0,Math.min(100,(notes-lower)/(upper-lower)*100)):100;$('rankProgressBar').style.width=progress+'%';$('rankProgressFoot').textContent=next?`${fmt(notes)} / ${fmt(next[0])} NOTES`:`${fmt(notes)} NOTES`;}$('rankProgress').classList.remove('hidden');
 $('combo').textContent=rushHits+'回';$('combo').title=rushHits>=12?'ULTIMATE CHAIN':rushHits>=8?'SUPER CHAIN':rushHits>=4?'HIGH CHAIN':'RUSH CHAIN';
 $('holds').innerHTML=holds.map((h,i)=>`<div class="gem ${h} ${i===0?'active':''}" title="${h}"></div>`).join('');
 $('start').classList.toggle('hidden',inRush||ended);$('start').disabled=started||inRush||ended;$('hold').classList.toggle('hidden',!inRush||ended);
 $('rushModePanel').classList.toggle('active',inRush&&!ended);$('normalModePanel').classList.toggle('hidden',inRush||ended);$('rushMode').disabled=ended;
 $('rushModeDescription').textContent=rushModeDescription(rushMode);
 $('hint').textContent=inRush?(st>0?'長押しで保留追加｜ST116回＋残保留4個｜最終10＋残保留4回転（最大14回転）は専用BGM':'残保留消化中｜新しい保留は追加できません｜最終局面専用BGM'):(timeMode?`時短中：残り${TIME_SPINS-timeSpins}回転｜大当たりで6,000 NOTES＋RUSH`:'通常モード：1回のタップで1回抽選');
 const pityLeft=Math.max(0,PITY_SPINS-normalStreak),pityBox=$('pityCountdown');
 pityBox.classList.toggle('hidden',inRush||timeMode||ended||normalStreak===0||pityLeft>PITY_SPINS);
 if(!pityBox.classList.contains('hidden')){$('pityCountdownText').textContent=`遊タイムまで 残り ${pityLeft} 回転`;$('pityCountdownBar').style.width=`${Math.max(0,Math.min(100,(PITY_SPINS-pityLeft)/PITY_SPINS*100))}%`;pityBox.classList.toggle('urgent',pityLeft<=10);}
 $('mode').textContent=inRush?`RUSH MODE ／ ${rushPhase()} ／ ${rushHits} CHAIN`:timeMode?`TIME MODE ／ ${TIME_SPINS-timeSpins}回転`:'NORMAL MODE';$('mode').className=inRush?'eyebrow rush':timeMode?'eyebrow time-mode':'eyebrow';
 document.body.dataset.mode='premium';document.body.dataset.phase=inRush?rushPhase().toLowerCase().replaceAll(' ','-'):timeMode?'time-mode':'normal';
 document.body.dataset.chain=rushHits>=12?'12-plus':rushHits>=8?'8-11':rushHits>=4?'4-7':'1-3';
}
async function endGame(){ended=true;inRush=false;clearInterval(consumeTimer);stopFinalBgm();stopHold();$('hold').disabled=true;showResult();update()}
async function activatePityTime(){
 timeMode=true;timeSpins=0;normalStreak=0;initialCategory='TIME MODE';
 jackpotAnimating=true;update();$('screen').classList.add('time-entry','pity-burst');
 $('number').textContent='TIME';$('number').className='number pityFlash';
 playTone(180,.22,'triangle',.08);await sleep(220);playTone(260,.24,'triangle',.08);await sleep(220);
 playTone(390,.55,'sine',.09);$('message').textContent='遊タイム突入！ 131回転の時短へ';
 $('message').className='message jackpot';await sleep(1000);
 $('screen').classList.remove('time-entry','pity-burst');$('number').classList.remove('pityFlash');
 jackpotAnimating=false;update();
}
async function timeSpinPresentation(isHit){
 const screen=$('screen');screen.classList.add('time-spin');
 $('message').textContent='TIME CHANCE';playTone(520,.12,'triangle',.05);
 for(let i=0;i<8;i++){ $('number').textContent=(50+visualRandom()*50).toFixed(3);await sleep(55); }
 screen.classList.remove('time-spin');$('message').textContent=isHit?'TIME JACKPOT！':'';
}
async function normalDraw(){
 if(started||inRush||ended||jackpotAnimating)return;
 started=true;unlockAudio();if(initialSpins===0)playDate=new Date();initialSpins++;
 initial=VALUES[Math.floor(Math.random()*VALUES.length)];initialTriple=triple(initial);
 $('number').className='number pulse';$('message').textContent='';update();
 if(timeMode){
  timeSpins++;await timeSpinPresentation(Boolean(initialTriple));
  if(initialTriple){
   initialPayout=PITY_PAYOUT;initialCategory='TIME JACKPOT';notes+=PITY_PAYOUT;payouts[PITY_PAYOUT]++;
   initialTriple=initialTriple;timeMode=false;normalStreak=0;
   notifyAchievement('TIME MODE');notifyAchievement('PREMIUM');evaluateThresholdAchievements();
   rushHits=0;combo=0;maxCombo=0;rushMode='STANDARD';$('rushMode').value='STANDARD';
   inRush=true;st=ST_MAX;segmentSpins=0;reserveSpins=0;jackpotAnimating=true;update();
   await jackpotEffect(initialTriple,PITY_PAYOUT,true);jackpotAnimating=false;
   $('message').innerHTML=`TIME JACKPOT！ <span class="${payoutClass(PITY_PAYOUT)}">+${fmt(PITY_PAYOUT)} NOTES</span> RUSH確定`;
   $('message').className='message jackpot';update();scheduleConsume();
  }else if(timeSpins>=TIME_SPINS){
   timeMode=false;timeSpins=0;normalStreak=0;started=false;
   $('number').textContent='---.---';$('message').textContent='時短終了｜通常モードへ';update();
  }else{started=false;update();}
  return;
 }
 normalStreak++;await normalSpinPresentation(Boolean(initialTriple));setOverallDisplay(initial);$('number').className='number pulse';
 if(initialTriple){
  normalStreak=0;rushHits=0;combo=0;maxCombo=0;rushMode='STANDARD';$('rushMode').value='STANDARD';
  if(initialSpins===1)notifyAchievement('QUICK START');
  if(initialPayout===6000)notifyAchievement('PREMIUM');
  initialPayout=initialAward(initialTriple);
  initialCategory=initialTriple==='000'?'ZERO JACKPOT':(initialTriple[0]==='7'?'SEVEN JACKPOT':(Number(initialTriple[0])%2===0?'EVEN JACKPOT':'ODD JACKPOT'));
  notes+=initialPayout;payouts[initialPayout]++;evaluateThresholdAchievements();
  inRush=true;st=ST_MAX;segmentSpins=0;reserveSpins=0;jackpotAnimating=true;update();
  await jackpotEffect(initialTriple,initialPayout,true);jackpotAnimating=false;
  $('message').innerHTML=`${initialTriple} JACKPOT！ <span class="${payoutClass(initialPayout)}">+${fmt(initialPayout)} NOTES</span>`;
  $('message').className='message jackpot';update();scheduleConsume();
 }else if(normalStreak>=PITY_SPINS){
  await activatePityTime();started=false;update();
 }else{started=false;$('message').textContent='';$('message').className='message';update();}
}
function addHold(){
 if(!inRush||ended||jackpotAnimating||st<=0||holds.length>=5||segmentSpins+holds.length>=ST_MAX+4)return;
 const color=weighted(baseColors);holds.push(color);const holdNode=$('holds');holdNode.classList.add('white-flash');setTimeout(()=>holdNode.classList.remove('white-flash'),180);
 const tones={blue:520,green:660,red:880,gold:1120,rainbow:1480};playTone(tones[color]||520,.16,'sine',.055);
 // 先読みは保留色に応じた雰囲気演出のみ。大当たりの確定告知とは区別する。
 // 保留入賞時は文章による告知を行わず、色と小さな光だけで示す。
 update();
}
function startHold(e){e.preventDefault();unlockAudio();if(holdTimer||!inRush)return;addHold();holdTimer=setInterval(addHold,500)}
function stopHold(){if(holdTimer){clearInterval(holdTimer);holdTimer=null}}
let consuming=false,finalBgmTimer=null,finalBgmStep=0;
const sleep=ms=>new Promise(resolve=>setTimeout(resolve,Math.round(ms*1.25)));let audioCtx=null,audioVolume=.55;function unlockAudio(){try{audioCtx=audioCtx||new (window.AudioContext||window.webkitAudioContext)();if(audioCtx.state==='suspended')audioCtx.resume()}catch(e){}}function playTone(freq,duration=.12,type='sine',gain=.045){try{unlockAudio();const o=audioCtx.createOscillator(),g=audioCtx.createGain();o.type=type;o.frequency.value=freq;g.gain.value=gain*audioVolume;o.connect(g);g.connect(audioCtx.destination);o.start();g.gain.exponentialRampToValueAtTime(.0001,audioCtx.currentTime+duration);o.stop(audioCtx.currentTime+duration)}catch(e){}}function jackpotSound(){[660,880,1100,1320].forEach((f,i)=>setTimeout(()=>playTone(f,.32,'sawtooth',.07),i*90))}
function startFinalBgm(){if(finalBgmTimer)return;const notesSeq=[220,277,330,277,247,330,370,330,277,247,220,165];finalBgmStep=0;const tick=()=>{const f=notesSeq[finalBgmStep%notesSeq.length];playTone(f,.34,'triangle',.028);if(finalBgmStep%4===0)playTone(f/2,.42,'sine',.035);finalBgmStep++;};tick();finalBgmTimer=setInterval(tick,560);}
function stopFinalBgm(){if(finalBgmTimer){clearInterval(finalBgmTimer);finalBgmTimer=null;}finalBgmStep=0;}
async function specialWinSound(mode){
 // Web Audioで合成するオリジナル音。既存作品の音源・旋律は使用しない。
 const seq=mode==='SHADOW'?[[110,.34,'sawtooth'],[165,.30,'sawtooth'],[220,.28,'triangle'],[330,.62,'sawtooth'],[440,.55,'triangle']]:mode==='IMPACT'?[[65,.22,'sawtooth'],[130,.24,'square'],[260,.28,'sawtooth'],[520,.55,'triangle'],[780,.50,'sine']]:[[55,.42,'sawtooth'],[0,.12,'sine'],[880,.20,'square'],[1320,.26,'triangle'],[1760,.72,'sine']];
 seq.forEach(([f,d,t],i)=>setTimeout(()=>{if(f)playTone(f,d,t,.10);},seq.slice(0,i).reduce((a,v)=>a+v[1]*1000,0)));
 await sleep(seq.reduce((a,v)=>a+v[1]*1000,0)+80);
}
function specialMissSound(mode){if(mode==='IMPACT'){playTone(72,.20,'sawtooth',.07);playTone(190,.16,'square',.035);}else{playTone(58,.32,'sine',.035);}}
function specialEventRate(color){return SPECIAL_EVENT_RATES[color]||0;}
function shouldShowSpecialEvent(color,hit){
 const p=COLOR_HIT_RATES[color],q=specialEventRate(color);if(!q||p<=0||p>=1)return false;
 // P(hit | event)=40%になるよう、当たり/外れそれぞれのイベント選択率を逆算。
 const conditional=hit?(q*.40/p):(q*.60/(1-p));return visualRandom()<Math.max(0,Math.min(1,conditional));
}
async function rushSpecialPresentation(hit){
 const mode=rushMode,screen=$('screen'),number=$('number');if(mode==='STANDARD')return;
 const triggered=shouldShowSpecialEvent(currentHoldColor,hit);if(!triggered)return;
 screen.classList.remove('rush-shadow','rush-lunge','rush-impact','rush-special-win','rush-special-miss');
 if(mode==='SHADOW'){number.textContent='';number.classList.add('blackout');screen.classList.add('rush-shadow');}else if(mode==='ONE_PUSH'){number.textContent='';number.classList.add('blackout');screen.classList.add('rush-one-push');}else if(mode==='IMPACT'){number.classList.add('pulse');}
 if(mode==='SHADOW'){await sleep(420);screen.classList.add('rush-lunge');await sleep(420);}
 else if(mode==='IMPACT'){screen.classList.add('rush-impact');playTone(52,.34,'sawtooth',.09);for(let i=0;i<7;i++){number.textContent=String(Math.floor(visualRandom()*10))+String(Math.floor(visualRandom()*10))+String(Math.floor(visualRandom()*10));await sleep(60);}number.classList.remove('pulse');}
 else if(mode==='ONE_PUSH'){
  const prompt=document.createElement('button');prompt.className='btn';prompt.type='button';prompt.textContent='PUSH';prompt.setAttribute('aria-label','ボタンを押して当落結果を表示');prompt.style.cssText='display:block;margin:14px auto;min-width:150px;font-size:20px';
  $('message').textContent='';screen.appendChild(prompt);await new Promise(resolve=>prompt.addEventListener('click',()=>{prompt.remove();resolve();},{once:true}));
  if(hit){screen.classList.add('rush-special-win');playTone(48,.24,'sawtooth',.11);const winSound=specialWinSound('ONE_PUSH');await winSound;}
  await sleep(220);
 }
 if(hit){if(mode!=='ONE_PUSH'){screen.classList.add('rush-special-win');await specialWinSound(mode);}await sleep(mode==='SHADOW'?350:280);}
 else{screen.classList.add('rush-special-miss');specialMissSound(mode);await sleep(340);}
 number.classList.remove('blackout','pulse');screen.classList.remove('rush-shadow','rush-one-push','rush-lunge','rush-impact','rush-special-win','rush-special-miss');$('message').textContent='';
}
function drumRoll(){unlockAudio();let i=0;const timer=setInterval(()=>{if(i++>18){clearInterval(timer);return}playTone(150+visualRandom()*90,.045,'square',.035);playTone(320+visualRandom()*160,.035,'triangle',.018)},55);return timer}function visualPayout(){const weights=[[300,20],[1500,50],[3000,15],[4500,10],[6000,5]];const a=new Uint32Array(1);crypto.getRandomValues(a);let n=a[0]%100;for(const [v,w] of weights){if(n<w)return v;n-=w;}return 1500;}
async function jackpotEffect(d,prize,isInitial=false){
 const mode=selectedMode,screen=$('screen'),number=$('number');
 screen.classList.remove('jackpot-simple','jackpot-balance','jackpot-premium','rush-shadow','rush-lunge','rush-impact','payout-300','payout-1500','payout-3000','payout-4500','payout-6000');
 screen.classList.add('jackpot-'+mode.toLowerCase());
 $('message').textContent='';number.classList.add('blackout');playTone(70,.45,'sawtooth',.08);

 // RUSH専用告知はconsume()内で当落表示前に実行する。ここでは確定後の祝福演出のみ行う。
 await sleep(760);
 number.classList.remove('blackout');setTripleDisplay(d);number.classList.add('rainbowFlash');screen.classList.add('burst');jackpotSound();
 $('message').textContent='';await sleep(520);
 if(isInitial){
   screen.classList.add('payout-'+prize);$('message').innerHTML=`JACKPOT！ <span class="${payoutClass(prize)}">+${fmt(prize)} NOTES</span>`;
   await sleep(1500);
 }else{
   $('message').textContent='RUSH BONUS';let stop=false;
   const stopButton=document.createElement('button');stopButton.className='btn secondary';stopButton.type='button';stopButton.textContent='ルーレットを停止';stopButton.style.display='block';stopButton.style.margin='8px auto';stopButton.onclick=()=>{stop=true};screen.appendChild(stopButton);
   let i=0;while(i<28&&!stop){const shown=visualPayout();$('message').innerHTML=`RUSH BONUS <b class="${payoutClass(shown)}">${fmt(shown)} NOTES</b>`;playTone(360+i*18,.055,'triangle',.025);await sleep(125+Math.floor(i/7)*18);i++;}
   stopButton.remove();screen.classList.add('payout-'+prize);$('message').innerHTML=`獲得出玉確定！ <span class="${payoutClass(prize)}">${fmt(prize)} NOTES</span>`;playTone(980,.25,'sine',.08);await sleep(1100);
 }
 screen.classList.remove('burst','jackpot-simple','jackpot-balance','jackpot-premium','rush-shadow','rush-lunge','rush-impact','rush-special-win','rush-special-miss','payout-300','payout-1500','payout-3000','payout-4500','payout-6000');number.classList.remove('rainbowFlash');
}
function scheduleConsume(){clearInterval(consumeTimer);if(inRush&&!ended&&!jackpotAnimating){const finalPhase=st<=10; if(finalPhase)startFinalBgm();else stopFinalBgm();consumeTimer=setInterval(consume,finalPhase?1900:800)}}
async function showDigits(digits){$('number').textContent='';for(let i=0;i<3;i++){const current=$('number').textContent; $('number').textContent=current+(digits[i]); await sleep(165);}setTripleDisplay(digits);}
async function consume(){
 if(!inRush||ended||jackpotAnimating||consuming||!holds.length)return;
 consuming=true;currentHoldColor=holds[0];let color=currentHoldColor,upgraded=false;
 if(color!=='rainbow'&&Math.random()<1/50){const order=['blue','green','red','gold','rainbow'];color=order[order.indexOf(color)+1];upgraded=true;holds[0]=color;update();playTone(920,.2,'triangle',.07);await sleep(300);}
 holds.shift();const finalPhase=st<=10||st===0;if(st>0){st--;segmentSpins++;}else{reserveSpins++;}rushSpins++;playTone(240,.09,'square',.035);if(st<=10){startFinalBgm();clearInterval(consumeTimer);consumeTimer=setInterval(consume,1900);}
 const hit=colorHit(color);currentHoldColor=color;
 await rushSpecialPresentation(hit);
 if(hit){
  const p=payout();if(color==='rainbow')rainbowHit=true;rushPayoutsWon.push(p);if(p===6000)notifyAchievement('PREMIUM');
  combo++;maxCombo=Math.max(maxCombo,combo);rushHits++;update();if(rushHits===10)notifyAchievement('RUSH MASTER');if(rushHits===20)notifyAchievement('RUSH LEGEND');
  rushNotes+=p;notes+=p;payouts[p]++;evaluateThresholdAchievements();st=ST_MAX;segmentSpins=0;reserveSpins=0;stopFinalBgm();jackpotAnimating=true;stopHold();clearInterval(consumeTimer);$('hold').disabled=true;
  const winning=String(Math.floor(visualRandom()*10)).repeat(3);$('number').className='number pulse';if(finalPhase){stopFinalBgm();$('screen').classList.add('last-ten-jackpot');playTone(92,.45,'sawtooth',.10);await sleep(900);}
  await jackpotEffect(winning,p,false);$('screen').classList.remove('last-ten-jackpot');
  $('message').innerHTML=`<span class="rush-chain-badge">CHAIN ${rushHits}</span> JACKPOT！ <span class="${payoutClass(p)}">+${fmt(p)} NOTES</span>`;$('message').className='message jackpot pulse';update();jackpotAnimating=false;
  if(inRush&&!ended){$('hold').disabled=false;scheduleConsume();}
 }else{
  const losing=missDigits();await showDigits(losing);$('number').className='number pulse';
  if(st<=0&&(reserveSpins>=4||holds.length===0)){holds=[];stopFinalBgm();$('message').textContent='RUSH END';update();consuming=false;endGame();return;}
  $('message').textContent='';$('message').className='message';
 }
 consuming=false;update();
}
function topPercentile(totalNotes){
 if(!SIMULATION_COUNT||!Array.isArray(PERCENTILE_DATA)||!PERCENTILE_DATA.length)return null;
 let atOrAbove=0;
 for(const item of PERCENTILE_DATA){if(Number(item.total_notes)>=Number(totalNotes))atOrAbove+=Number(item.count)||0;}
 return Math.max(0,Math.min(100,atOrAbove/SIMULATION_COUNT*100));
}
function percentileLabel(totalNotes){const value=topPercentile(totalNotes);return value===null?'算出不可':`上位${value.toFixed(1)}%`;}
function showResult(){
 const total=notes, resultRank=rankFor(total), totalHits=Object.values(payouts).reduce((a,b)=>a+b,0);
 const colors={6000:'#a987ff',4500:'#ff5c78',3000:'#e85c86',1500:'#f2c83f',300:'#249cff'};
 const pieStops=[];let offset=0;[6000,4500,3000,1500,300].forEach(k=>{const v=payouts[k];if(v>0){const end=offset+v/Math.max(1,totalHits)*100;pieStops.push(`${colors[k]} ${offset}% ${end}%`);offset=end;}});
 const legend=[6000,4500,3000,1500,300].map(k=>`<div><i class="rc-dot" style="background:${colors[k]}"></i><span>${fmt(k)} NOTES：${payouts[k]}回</span></div>`).join('');
 const pieLabels=(()=>{let a=-Math.PI/2;let out='';[6000,4500,3000,1500,300].forEach(k=>{const v=payouts[k];if(!v||!totalHits)return;const pct=v/totalHits*100;const b=a+v/totalHits*Math.PI*2;const mid=(a+b)/2;const inside=pct>=4.5;const r=inside?49:68;const rawX=75+Math.cos(mid)*r,rawY=75+Math.sin(mid)*r;const cx=Math.max(12,Math.min(138,rawX)),cy=Math.max(12,Math.min(138,rawY));const label=pct<0.1?'<0.1%':pct.toFixed(1)+'%';if(!inside){const x1=75+Math.cos(mid)*50,y1=75+Math.sin(mid)*50,x2=75+Math.cos(mid)*59,y2=75+Math.sin(mid)*59;out+=`<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="#fff" stroke-width="1"/>`;}out+=`<text x="${cx.toFixed(1)}" y="${(cy+3).toFixed(1)}" font-size="${inside?10:9}">${label}</text>`;a=b;});return out;})();
 const percentile=percentileLabel(total);
 const initialRows=[['初当たり回転数',''+initialSpins+'回転'],['初当たりOVERALL',initial===null?'--.---':Number(initial).toFixed(3)],['初当たり区分',initialCategory],['初当たり獲得',`<span class="${payoutClass(initialPayout)}">${fmt(initialPayout)} NOTES</span>`]];
 const rushRows=[['RUSH大当たり',`${rushHits}回`],['RUSH獲得NOTES',`<span class=\"${notesColor(rushNotes)}\">${fmt(rushNotes)} NOTES</span>`],['RUSH消化回転数',`${rushSpins}回`]];
 const rowHtml=arr=>arr.map(([k,v])=>`<div class="rc-row"><span>${k}</span><b>${v}</b></div>`).join('');
 $('resultGrid').innerHTML=`
 <div class="rc-card-brand">OVERALL PACHINKO</div>
 <div class="resultCardHead">
  <section class="rc-panel"><div class="rc-title">OVERALL ／ 総獲得</div><div style="display:grid;grid-template-columns:1fr auto;align-items:center;gap:10px"><div><div style="font-weight:800">総獲得NOTES</div><div class="rc-total ${notesColor(total)}">${fmt(total)} <small>NOTES</small></div></div><div style="border-left:2px solid #d9b83e;padding-left:16px;text-align:center"><div style="font-weight:900">RANK</div><div class="rc-rank rank-${rankColor(resultRank)}">${resultRank}</div></div></div></section>
  <section class="rc-panel"><div class="rc-title">SIMULATION ／ 100万件中の位置</div><div class="rankline" style="text-align:center;margin-top:22px">${percentile}</div><div class="rc-sub" style="text-align:center">${SIMULATION_COUNT.toLocaleString('ja-JP')}件のシミュレーション結果との比較</div></section>
 </div>
 <div class="rc-body">
  <section class="rc-panel rc-pink"><div class="rc-title">初当たり ／ 基本情報</div><div class="rc-rows">${rowHtml(initialRows)}</div></section>
  <section class="rc-panel rc-cyan"><div class="rc-title">RUSH ／ 連チャン情報</div><div class="rc-rows">${rowHtml(rushRows)}</div><div class="rc-average">RUSH獲得平均出玉<strong>${rushHits?fmt(Math.round(rushNotes/rushHits))+' NOTES':'—'}</strong></div></section>
  <section class="rc-panel rc-gold rc-payout"><div class="rc-title">出玉振り分け ／ 当選結果の内訳</div><div class="rc-piearea"><div class="rc-piewrap"><div class="rc-pie" style="background:${totalHits?`conic-gradient(${pieStops.join(',')})`:'#30283a'}"></div><svg class="rc-pie-labels" viewBox="0 0 150 150" aria-hidden="true">${pieLabels}</svg></div><div class="rc-legend">${legend}</div></div></section>
 </div>
 <section class="rc-footer"><div class="rc-date">プレイ日時：${playDate.toLocaleString('ja-JP')}</div></section>
 `;
 $('result').classList.remove('hidden');
}
function reset(){clearInterval(consumeTimer);stopFinalBgm();stopHold();rushMode='STANDARD';$('rushMode').value='STANDARD';earnedAchievements=[];rushPayoutsWon=[];rainbowHit=false;selectedMode='PREMIUM';normalMode='STANDARD';$('normalMode').value='STANDARD';$('normalModeDescription').textContent=normalModeDescription('STANDARD');notes=0;started=false;inRush=false;timeMode=false;timeSpins=0;normalStreak=0;ended=false;st=0;segmentSpins=0;reserveSpins=0;holds=[];initialSpins=0;combo=0;maxCombo=0;rushHits=0;rushNotes=0;rushSpins=0;initial=0;initialTriple=null;initialCategory='MISS';initialPayout=0;payouts={6000:0,4500:0,3000:0,1500:0,300:0};$('number').textContent='---.---';$('achievementToast').classList.remove('show');$('message').textContent='STARTを押して抽選';$('message').className='message';$('result').classList.add('hidden');$('savePreview').classList.add('hidden');$('savedResultImage').removeAttribute('src');$('hold').disabled=false;$('start').disabled=false;update()}
document.addEventListener('contextmenu',e=>{if(e.target.closest('.holdButton'))e.preventDefault()});document.addEventListener('selectstart',e=>{if(e.target.closest('.holdButton'))e.preventDefault()});$('start').addEventListener('pointerdown',unlockAudio,{passive:true});$('start').addEventListener('click',normalDraw);$('hold').addEventListener('contextmenu',e=>e.preventDefault());$('hold').addEventListener('selectstart',e=>e.preventDefault());$('hold').addEventListener('pointerdown',startHold);['pointerup','pointerleave','pointercancel','lostpointercapture'].forEach(e=>window.addEventListener(e,stopHold));$('replay').addEventListener('click',reset);$('rushMode').addEventListener('change',e=>{rushMode=['STANDARD','SHADOW','IMPACT','ONE_PUSH'].includes(e.target.value)?e.target.value:'STANDARD';$('rushModeDescription').textContent=rushModeDescription(rushMode);update();});$('normalMode').addEventListener('change',e=>{normalMode=['STANDARD','FORESHADOW','QUICK'].includes(e.target.value)?e.target.value:'STANDARD';$('normalModeDescription').textContent=normalModeDescription(normalMode);});$('volume').addEventListener('input',e=>{audioVolume=Number(e.target.value)/100;$('volumeValue').textContent=e.target.value+'%'});
$('save').addEventListener('click',()=>{
 const c=document.createElement('canvas');c.width=1600;c.height=1200;let x=c.getContext('2d');
 const wrapCardText=(value,maxChars)=>{const chars=Array.from(String(value));const lines=[];for(let i=0;i<chars.length;i+=maxChars)lines.push(chars.slice(i,i+maxChars).join(''));return lines.length?lines:[''];};
 const dateLines=wrapCardText('プレイ日時：'+playDate.toLocaleString('ja-JP'),64);
 const footerY=800,footerHeight=Math.max(100,58+dateLines.length*25),brandY=footerY+footerHeight+115;
 const bg=x.createRadialGradient(800,360,80,800,600,1000);bg.addColorStop(0,'#24162f');bg.addColorStop(.7,'#100d1b');bg.addColorStop(1,'#080711');x.fillStyle=bg;x.fillRect(0,0,1600,1200);
 x.strokeStyle='#d9b83e';x.lineWidth=10;x.strokeRect(20,20,1560,1160);
 const panel=(a,b,w,h,color='#d9b83e')=>{x.lineWidth=5;x.strokeStyle=color;x.fillStyle='#171020';x.beginPath();x.roundRect(a,b,w,h,18);x.fill();x.stroke()};
 const txt=(t,a,b,size=30,color='#f8f4e8',weight='bold',align='left')=>{x.font=`${weight} ${size}px sans-serif`;x.fillStyle=color;x.textAlign=align;x.fillText(t,a,b)};
 const rankPal={'rainbow':['#ff5c5c','#ffcf5c','#75e58b','#61caff','#a987ff','#ff78d2'],'gold':['#f5c84b'],'red':['#f05b70'],'blue':['#57aaff'],'green':['#5bd18b'],'pink':['#ff91bd'],'purple':['#bd83ee'],'gray':['#a5a5a5']};
 const drawGradient=(colors,a,b)=>{if(colors.length===1)return colors[0];const g=x.createLinearGradient(a,0,b,0);colors.forEach((v,i)=>g.addColorStop(i/(colors.length-1),v));return g};
 txt('OVERALL PACHINKO',55,75,48,'#f5d77b');x.strokeStyle='#e8c64f';x.lineWidth=4;x.beginPath();x.moveTo(55,95);x.lineTo(1545,95);x.stroke();
 panel(45,120,900,260);panel(965,120,590,260);
 txt('OVERALL ／ 総獲得',75,165,30,'#f5d65d');txt('総獲得NOTES',85,220,26);
 const totalColor=notes>=10000?drawGradient(rankPal.rainbow,90,450):notes>=5000?'#e9c45a':'#c5cbd4';txt(fmt(notes),85,320,94,totalColor);txt('NOTES',480,320,34);
 txt('RANK',760,220,28,'#fff','bold','center');txt(rankFor(notes),760,320,88,drawGradient(rankPal[rankColor(rankFor(notes))]||['#fff'],650,870),'bold','center');
 txt('SIMULATION ／ 100万件中の位置',995,165,29,'#f5d65d');txt(percentileLabel(notes),1260,260,44,'#79dcff','bold','center');txt(`${SIMULATION_COUNT.toLocaleString('ja-JP')}件のシミュレーション結果との比較`,1260,310,20,'#f8f4e8','normal','center');
 panel(45,405,490,370,'#e66ab1');panel(555,405,490,370,'#54d6e4');panel(1065,405,490,370);
 txt('初当たり ／ 基本情報',75,450,28,'#f18bc8');
 const leftLines=[['初当たり',initialSpins+'回転'],['初当たりOVERALL',initial===null?'--.---':Number(initial).toFixed(3)],['初当たり区分',initialCategory],['初当たり獲得',fmt(initialPayout)+' NOTES']];
 leftLines.forEach((v,i)=>{const yy=510+i*62;txt(v[0],75,yy,24);const initialColor=i===3?(initialPayout===300?'#57aaff':initialPayout===1500?'#f5c84b':drawGradient(rankPal.rainbow,320,500)):'#fff';txt(v[1],500,yy,24,initialColor,'bold','right');x.strokeStyle='#65556e';x.lineWidth=2;x.beginPath();x.moveTo(75,yy+17);x.lineTo(505,yy+17);x.stroke()});
 txt('RUSH ／ 連チャン情報',585,450,28,'#71e8ee');
 const rushLines=[['RUSH大当たり',rushHits+'回'],['RUSH獲得NOTES',fmt(rushNotes)],['RUSH消化回転数',rushSpins+'回']];
 rushLines.forEach((v,i)=>{const yy=510+i*62;txt(v[0],585,yy,24);const rushValColor=i===1?(rushNotes>=10000?drawGradient(rankPal.rainbow,700,1000):rushNotes>=5000?'#e9c45a':'#c5cbd4'):'#fff';txt(v[1],1010,yy,24,rushValColor,'bold','right');x.strokeStyle='#65556e';x.lineWidth=2;x.beginPath();x.moveTo(585,yy+17);x.lineTo(1015,yy+17);x.stroke()});
 panel(575,690,450,65);txt('RUSH獲得平均出玉',800,718,22,'#f5d65d','bold','center');txt(rushHits?Math.round(rushNotes/rushHits).toLocaleString('ja-JP')+' NOTES':'—',800,746,25,'#fff','bold','center');
 txt('出玉振り分け ／ 当選結果の内訳',1095,450,26,'#f5d65d');
 const keys=[6000,4500,3000,1500,300],cols={6000:'#a987ff',4500:'#ff5c78',3000:'#e85c86',1500:'#f2c83f',300:'#249cff'};
 const hitTotal=keys.reduce((a,k)=>a+payouts[k],0);let angle=-Math.PI/2;const cx=1195,cy=610,r=120;
 x.beginPath();x.arc(cx,cy,r,0,Math.PI*2);x.fillStyle='#30283a';x.fill();
 if(hitTotal){for(const k of keys){const n=payouts[k];if(!n)continue;const next=angle+n/hitTotal*Math.PI*2;x.beginPath();x.moveTo(cx,cy);x.arc(cx,cy,r,angle,next);x.closePath();x.fillStyle=cols[k];x.fill();
 const pct=n/hitTotal*100,mid=(angle+next)/2,inside=pct>=4.5,rr=inside?78:145;
 let tx=cx+Math.cos(mid)*rr,ty=cy+Math.sin(mid)*rr;
 if(!inside){tx=Math.max(1100,Math.min(1295,tx));ty=Math.max(485,Math.min(745,ty));x.beginPath();x.moveTo(cx+Math.cos(mid)*r,cy+Math.sin(mid)*r);x.lineTo(tx,ty);x.strokeStyle='#fff';x.lineWidth=2;x.stroke();}
 x.font=`bold ${inside?18:15}px sans-serif`;x.textAlign='center';x.textBaseline='middle';
 x.lineWidth=4;x.strokeStyle='#24172e';x.strokeText(pct<0.1?'<0.1%':pct.toFixed(1)+'%',tx,ty);
 x.fillStyle='#fff';x.fillText(pct<0.1?'<0.1%':pct.toFixed(1)+'%',tx,ty);
 angle=next;}}
 keys.forEach((k,i)=>{const yy=500+i*48;x.fillStyle=cols[k];x.fillRect(1335,yy-18,22,22);txt(`${fmt(k)} NOTES：${payouts[k]}回`,1368,yy,19,'#f8f4e8','normal')});
 panel(45,footerY,1510,footerHeight);txt('PLAY DATE ／ プレイ日時',75,footerY+38,22,'#f5d65d');
 dateLines.forEach((line,i)=>txt(line,85,footerY+72+i*25,17,'#f8f4e8','normal'));
 
 const finishCardImage=()=>{const dataUrl=c.toDataURL('image/png');$('savedResultImage').src=dataUrl;$('savePreview').classList.remove('hidden');$('savePreview').scrollIntoView({behavior:'smooth',block:'center'});if(!/iPhone|iPad|iPod/.test(navigator.userAgent)){const a=document.createElement('a');a.download='overall_pachinko_result.png';a.href=dataUrl;a.click();}};
 finishCardImage();
});
function xWeightedLength(text){const urlPattern=/https?:\/\/[^\s]+/g;let total=0,last=0,match;while((match=urlPattern.exec(text))!==null){total+=Array.from(text.slice(last,match.index)).reduce((n,ch)=>n+(ch.codePointAt(0)<=0x10ff?1:((ch.codePointAt(0)===0x200d||ch.codePointAt(0)===0xfe0f||ch.codePointAt(0)===0xfe0e)?0:2)),0)+23;last=match.index+match[0].length;}return total+Array.from(text.slice(last)).reduce((n,ch)=>n+(ch.codePointAt(0)<=0x10ff?1:((ch.codePointAt(0)===0x200d||ch.codePointAt(0)===0xfe0f||ch.codePointAt(0)===0xfe0e)?0:2)),0);}
function fitXText(lines){
 const limit=220, url=lines.find(line=>/^https?:\/\//.test(line))||APP_URL;
 const tags=lines.find(line=>line.startsWith('#'))||'#OVERALLPACHINKO';
 const title=lines[0]||'🎰 OVERALL PACHINKO 結果';
 const score=lines[1]||`総獲得NOTES：${fmt(notes)}（${rankFor(notes)}）`;
 const optional=lines.slice(2).filter(line=>line!==url&&line!==tags);
 let kept=[title,score,...optional,tags,url];
 let text=kept.join('\n');
 // まず情報量の大きい補足行から省き、称号・タグ・URLは残す。
 const dropPrefixes=['RUSH消化：','初当たり出玉：','初当たり：','シミュレーション位置：','RUSH大当たり：'];
 for(const prefix of dropPrefixes){
   if(xWeightedLength(text)<=limit)break;
   const idx=kept.findIndex(line=>line.startsWith(prefix));
   if(idx>=0){kept.splice(idx,1);text=kept.join('\n');}
 }
 // 称号は最大3件＋ほか○件。さらに必要なら称号行自体を省略する。
 if(xWeightedLength(text)>limit){
   const idx=kept.findIndex(line=>line.startsWith('獲得称号：'));
   if(idx>=0){kept.splice(idx,1);text=kept.join('\n');}
 }
 // URL・ハッシュタグを維持したまま本文を短縮。固定部分だけで超過する場合も安全に切り詰める。
 if(xWeightedLength(text)>limit){
   const fixed=[title,score,tags,url].join('\n');
   let shortScore=score;
   while(xWeightedLength([title,shortScore,tags,url].join('\n'))>limit && Array.from(shortScore).length>8){
     shortScore=Array.from(shortScore).slice(0,-1).join('');
   }
   text=[title,shortScore,tags,url].join('\n');
 }
 if(xWeightedLength(text)>limit){
   // 最終保護：URLとハッシュタグは保持し、タイトル・スコアを短縮する。
   const suffix='\n'+tags+'\n'+url;
   let prefix='OVERALL '+fmt(notes)+' NOTES';
   while(xWeightedLength(prefix+suffix)>limit&&prefix.length>1)prefix=prefix.slice(0,-1);
   text=prefix+suffix;
 }
 return text;
}
$('share').addEventListener('click',()=>{
 const lines=['🎰 OVERALL PACHINKO 結果',`総獲得NOTES：${fmt(notes)}（${rankFor(notes)}）`];
 lines.push(`シミュレーション位置：${percentileLabel(notes)}`);
 const earned=achievementList();
 if(earned.length)lines.push('獲得称号：'+earned.slice(0,3).join('・')+(earned.length>3?` ほか${earned.length-3}件`:''));
 lines.push(`初当たり：${initialSpins}回転／OVERALL ${initial===null?'--.---':Number(initial).toFixed(3)}`,`初当たり出玉：${fmt(initialPayout)} NOTES（${initialCategory}）`,`RUSH大当たり：${rushHits}回／RUSH獲得：${fmt(rushNotes)} NOTES`,`RUSH消化：${rushSpins}回転`,'#OVERALLPACHINKO',APP_URL);
 const t=fitXText(lines),weighted=xWeightedLength(t);
 if(weighted>220){console.error('X share length guard failed',weighted);return;}
 window.open('https://twitter.com/intent/tweet?text='+encodeURIComponent(t),'_blank','noopener');
});
update();
</script></body></html>'''
    html = (html.replace("__VALUES__", values_json).replace("__APPURL__", url_json)
            .replace("__PERCENTILE_DATA__", percentile_data_json).replace("__SIMULATION_COUNT__", str(simulation_count))
            .replace("__RANK_TIERS__", rank_tiers_json)
            .replace("__RUSH_PAYOUTS__", rush_payouts_json)
            .replace("__PITY_SPINS__", str(PITY_SPINS)).replace("__PITY_PAYOUT__", str(PITY_PAYOUT))
            .replace("__ST_MAX__", str(ST_MAX)).replace("__BASE_COLORS__", base_colors_json)
            .replace("__COLOR_HIT_RATES__", color_hit_rates_json)
            .replace("__SPECIAL_EVENT_RATES__", special_event_rates_json))

    components.html(html, height=1500, scrolling=True)
