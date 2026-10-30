#!/usr/bin/env python3
"""
Final Third — Dedicated Video SEO Pages & Category Hubs Generator
Generates:
1. 20 dedicated, accessible SEO video pages (14 Football, 6 Cricket)
2. Football category hub (/football/index.html) with 14 clickable video cards
3. Cricket category hub (/cricket/index.html) with 6 clickable video cards
4. Google Video XML Sitemap (sitemap.xml)
"""

import os
import json
import re

DOMAIN = "https://www.finalthird-haris.com"

VIDEOS = [
    # ========================== FOOTBALL (14) ==========================
    {
        "id": "MT7IaTzzwY4",
        "slug": "real-madrid-vs-barcelona-el-clasico-tactical-analysis",
        "sport": "football",
        "sport_title": "Football Analysis",
        "playlist": "Barcelona & Real Madrid",
        "title": "ക്യാമ്പ് നൗവിന് തീയിട്ട് ഹോസേ... ദാ ഈ റയലിനെ ഇനി പേടിച്ചോ ! Real Madrid vs Barcelona | Haris Nenmara",
        "seo_title": "Real Madrid vs Barcelona El Clasico Tactical Analysis | Final Third",
        "meta_desc": "In-depth tactical analysis of El Clasico between Real Madrid and Barcelona in Malayalam by Haris Nenmara. Dissecting match moments, tactical setups, and key plays.",
        "published_iso": "2026-10-26T09:41:12+00:00",
        "views": "114K views",
        "read_time": "3 min read",
        "p1_ml": "എൽ ക്ലാസിക്കോ പോരാട്ടത്തിൽ റയൽ മാഡ്രിഡും ബാഴ്സലോണയും നേർക്കുനേർ വന്നപ്പോൾ കളിക്കളത്തിൽ പിറന്നത് ആധുനിക ഫുട്ബോളിന്റെ ഏറ്റവും മികച്ച പോരാട്ടങ്ങളിലൊന്നാണ്. ക്യാമ്പ് നൗവിൽ നടന്ന മത്സരത്തിൽ റയൽ മാഡ്രിഡിന്റെ ഘടനയും കൗണ്ടർ-അറ്റാക്കിങ് വേഗവും ബാഴ്സയുടെ പ്രതിരോധത്തെ നിരന്തരം സമ്മർദ്ദത്തിലാക്കി. ഹോസെയുടെ തന്ത്രപരമായ നീക്കങ്ങളും ടീം ഷേപ്പും എങ്ങനെയെല്ലാമാണ് കളിയുടെ ഗതി മാറ്റിയതെന്ന് ഹാരിസ് നെന്മാറ ഈ വീഡിയോയിൽ കൃത്യമായി പരിശോധിക്കുന്നു.",
        "p2_en": "This tactical breakdown dissects the tactical setups of both European heavyweights in El Clasico. We examine how Real Madrid exploited transition spaces, the positioning of wingers to isolate defenders, and the intense midfield battle. Haris Nenmara breaks down why structural discipline and quick direct passes made the decisive difference in this high-voltage showdown.",
        "takeaways": [
            "Exploitation of transition spaces during rapid counter-attacking phases",
            "Midfield pressing triggers that disrupted opponent build-up play",
            "Wing play and isolated one-on-one attacking matchups",
            "Key defensive balance maintained across both halves"
        ],
        "tags": ["El Clasico", "Real Madrid", "Barcelona", "Football Analysis Malayalam", "Haris Nenmara", "Final Third"]
    },
    {
        "id": "RDpM-6xLCao",
        "slug": "barcelona-vs-real-madrid-hansi-flick-tactics",
        "sport": "football",
        "sport_title": "Football Analysis",
        "playlist": "Barcelona",
        "title": "ബാഴ്സയെ വീഴ്ത്താന്‍ കെല്‍പ്പുണ്ടോ റയലിന് ? Real madrid vs Barcelona | El clasico",
        "seo_title": "Can Real Madrid Beat Barcelona? El Clasico Match Analysis | Final Third",
        "meta_desc": "Can Real Madrid stop this in-form Barcelona squad? Comprehensive El Clasico tactical preview and match debrief in Malayalam by Haris Nenmara.",
        "published_iso": "2026-10-24T11:17:04+00:00",
        "views": "55K views",
        "read_time": "3 min read",
        "p1_ml": "യൂറോപ്യൻ ഫുട്ബോളിൽ പുതിയ ഊർജ്ജത്തോടെ കുതിക്കുന്ന ബാഴ്സലോണയെ തടഞ്ഞുനിർത്താൻ റയൽ മാഡ്രിഡിന് സാധിക്കുമോ? അതിവേഗത്തിലുള്ള ബോൾ റിക്കവറിയും ഒത്തിണക്കമുള്ള പ്രതിരോധവും അടിസ്ഥാനമാക്കിയുള്ള ബാഴ്സയുടെ ശൈലി ലാ ലിഗയിലെ ഏറ്റവും വലിയ ചോദ്യചിഹ്നമായി മാറിയിരിക്കുകയാണ്. എതിരാളികളുടെ പിഴവുകളെ വേഗത്തിൽ മുതലെടുക്കുന്ന നീക്കങ്ങൾ എൽ ക്ലാസിക്കോയിൽ എത്രത്തോളം നിർണ്ണായകമാകുമെന്ന് ഈ വീഡിയോ വ്യക്തമാക്കുന്നു.",
        "p2_en": "An analytical exploration of Barcelona's high-tempo football ahead of the El Clasico clash with Real Madrid. We evaluate their synchronized defensive discipline, fluid front-line combinations, and spatial dominance in the final third. The analysis investigates whether Real Madrid can exploit transition moments or if Barcelona's structural intensity will dictate the match.",
        "takeaways": [
            "Synchronized defensive line coordination and compact team shape",
            "Central counter-pressing enabling instant possession regain",
            "Movement of attacking midfielders into half-spaces to break low blocks",
            "Transition management against elite speed on the counter"
        ],
        "tags": ["Barcelona", "Real Madrid", "El Clasico", "La Liga", "Tactical Preview", "Haris Nenmara"]
    },
    {
        "id": "4LGjduzWzFg",
        "slug": "barcelona-vs-psg-lamine-yamal-ucl-tactics",
        "sport": "football",
        "sport_title": "Football Analysis",
        "playlist": "Barcelona & Champions League",
        "title": "PSG യെ വീഴ്ത്താൻ ആരുണ്ട് ഇവിടെ ? | Barcelona vs Psg | Lamine Yamal",
        "seo_title": "Barcelona vs PSG Champions League Tactical Analysis | Lamine Yamal Focus",
        "meta_desc": "UEFA Champions League tactical masterclass: Barcelona vs PSG. Detailed analysis of Lamine Yamal's wing play and tactical dynamics by Haris Nenmara.",
        "published_iso": "2026-10-21T13:36:26+00:00",
        "views": "55K views",
        "read_time": "3 min read",
        "p1_ml": "യുവേഫ ചാമ്പ്യൻസ് ലീഗിൽ ബാഴ്സലോണയും പാരീസ് സെന്റ് ജെർമെയ്നും (PSG) തമ്മിൽ നടന്ന തീപാറുന്ന പോരാട്ടത്തിന്റെ സമഗ്രമായ അവലോകനം. കൗമാര വിസ്മയം ലാമിൻ യമാലിന്റെ അസാധാരണമായ വിങ്-പ്ലേയും ഡ്രിബ്ലിങ് വൈദഗ്ധ്യവും പിഎസ്ജിയുടെ പ്രതിരോധ നിരയെ എങ്ങിനെ സമ്മർദ്ദത്തിലാക്കിയെന്ന് ഹാരിസ് നെന്മാറ വിശദീകരിക്കുന്നു. യൂറോപ്യൻ വമ്പന്മാരുടെ കളിക്കളത്തിലെ തന്ത്രപരമായ ഏറ്റുമുട്ടൽ ഇതിൽ കാണാം.",
        "p2_en": "Focusing on the Champions League blockbuster between Barcelona and PSG, this video analyzes tactical dynamics in high-stakes European football. Discover how Lamine Yamal's directness on the right flank stretched PSG's defensive shape, allowing runners to penetrate dangerous attacking pockets.",
        "takeaways": [
            "Lamine Yamal's 1v1 dribbling and box-entry creation",
            "Tactical overload strategies in the attacking third",
            "Midfield possession control under high European competition tempo",
            "Key defensive transitions in knockout European football"
        ],
        "tags": ["Barcelona vs PSG", "Champions League", "Lamine Yamal", "UCL Analysis", "Football Tactics", "Haris Nenmara"]
    },
    {
        "id": "ZoU-SU80SLM",
        "slug": "barcelona-lamine-yamal-rodri-hansi-flick-system",
        "sport": "football",
        "sport_title": "Football Analysis",
        "playlist": "Barcelona",
        "title": "ബാഴ്സയെ ആര് പിടിച്ച് കെട്ടും ? Barcelona | Lamine Yamal | Rodri | Hansi Flick",
        "seo_title": "Who Can Stop Barcelona? Lamine Yamal, Rodri & Hansi Flick System Analysis",
        "meta_desc": "Can anyone stop this Barcelona team? Tactical investigation into Hansi Flick's blueprint, Rodri comparisons, and Lamine Yamal's influence.",
        "published_iso": "2026-10-18T09:39:08+00:00",
        "views": "42K views",
        "read_time": "3 min read",
        "p1_ml": "ഈ സീസണിൽ യൂറോപ്പിലെ ഏറ്റവും ഫോമിലുള്ള ടീമുകളിലൊന്നായി ബാഴ്സലോണ മാറിയത് എങ്ങനെ? ഹാൻസി ഫ്ലിക്കിന്റെ ഫിറ്റ്നസ് സംസ്കാരവും മൈതാനത്തെ തീവ്രതയും യുവതാരങ്ങൾക്ക് നൽകുന്ന സ്വാതന്ത്ര്യവും ടീമിന്റെ ആത്മവിശ്വാസം ഉയർത്തിയിരിക്കുകയാണ്. ലാമിൻ യമാലിന്റെ മാന്ത്രികതയും റോഡ്രിയുടെ പ്ലേ-മേക്കിങ് സ്വാധീനവും ചേരുമ്പോൾ യൂറോപ്യൻ ഫുട്ബോളിൽ ബാഴ്സയെ പൂട്ടാൻ ആർക്ക് സാധിക്കും എന്ന ചോദ്യത്തിനുള്ള ഉത്തരമാണ് ഈ വിശകലനം.",
        "p2_en": "A comprehensive deep dive into the underlying metrics powering Barcelona's dominant run. We explore Hansi Flick's direct attacking verticality, intense counter-pressing metrics, and how young talents thrive within a defined tactical framework that balances high-risk defensive lines with relentless offensive output.",
        "takeaways": [
            "Vertical build-up speed replacing redundant lateral circulation",
            "High defensive pressing block winning possession in opponent's half",
            "Role of creative wingers in creating cutback and shooting angles",
            "Physical conditioning and endurance advantages in the second half"
        ],
        "tags": ["Barcelona", "Lamine Yamal", "Hansi Flick", "European Football", "Tactical System", "Final Third"]
    },
    {
        "id": "XMR4quSxjHw",
        "slug": "real-madrid-vs-rb-leipzig-tactical-preview",
        "sport": "football",
        "sport_title": "Football Analysis",
        "playlist": "Real Madrid",
        "title": "ബാഴ്സക്ക് അത്ര എളുപ്പമാകില്ല കാര്യങ്ങള്‍ ! Real Madrid vs RB Leipzig",
        "seo_title": "Real Madrid vs RB Leipzig Match Analysis & Champions League Lessons",
        "meta_desc": "Real Madrid vs RB Leipzig tactical match breakdown. Evaluating defensive solidity, pressing traps, and tactical adjustments in European football.",
        "published_iso": "2026-10-22T09:49:56+00:00",
        "views": "42K views",
        "read_time": "3 min read",
        "p1_ml": "യൂറോപ്യൻ ഫുട്ബോളിൽ ആർബി ലെയ്പ്സിഗിനെതിരായ റയൽ മാഡ്രിഡിന്റെ പോരാട്ടം നൽകിയ തന്ത്രപരമായ മുന്നറിയിപ്പുകൾ പരിശോധിക്കുകയാണ് ഹാരിസ് നെന്മാറ. ജർമ്മൻ ടീമിന്റെ ഹൈ-ഇന്റൻസിറ്റി പ്രസ്സിങ്ങിന് മുന്നിൽ റയൽ നേരിട്ട വെല്ലുവിളികളും, പ്രതിരോധത്തിലെ വിടവുകൾ നികത്താൻ നടത്തിയ തന്ത്രപരമായ മാറ്റങ്ങളും കളിയിലെ വഴിത്തിരിവുകളായി. ലാ ലിഗയിലെ മറ്റ് മത്സരങ്ങൾക്കും എൽ ക്ലാസിക്കോയ്ക്കും ഈ പോരാട്ടം നൽകുന്ന സന്ദേശങ്ങൾ എന്തൊക്കെയാണ്?",
        "p2_en": "Analyzing Real Madrid's resilience under tactical duress against RB Leipzig. This video studies how Leipzig's organized pressing challenged Madrid's circulation and how individual tactical moments from Madrid's decisive players salvaged momentum in crucial phases of the game.",
        "takeaways": [
            "Defensive mid-block transitions and counter-attack containment",
            "Individual ball-carrying impact under sustained pressure",
            "Tactical balance in high-tempo European knockout atmospheres",
            "Key lessons for Real Madrid heading into top-flight domestic clashes"
        ],
        "tags": ["Real Madrid", "RB Leipzig", "Champions League", "Tactical Breakdown", "Haris Nenmara", "Final Third"]
    },
    {
        "id": "9q0iwA1bpkI",
        "slug": "real-madrid-vs-roma-tactical-breakdown",
        "sport": "football",
        "sport_title": "Football Analysis",
        "playlist": "Real Madrid",
        "title": "റോമയെ എരിച്ചു ! പഠിക്കാൻ ഇനിയുമേറെ | Real Madrid Vs Roma",
        "seo_title": "Real Madrid vs Roma Tactical Breakdown | Final Third Football Analysis",
        "meta_desc": "Real Madrid vs AS Roma match debrief with Haris Nenmara. Comprehensive evaluation of attacking combinations, finishing efficiency, and tactical discipline.",
        "published_iso": "2026-10-20T12:00:00+00:00",
        "views": "57K views",
        "read_time": "3 min read",
        "p1_ml": "എഎസ് റോമയ്ക്കെതിരായ റയൽ മാഡ്രിഡിന്റെ ഗംഭീര പ്രകടനം ഫുട്ബോൾ പ്രേമികൾക്ക് സമ്മാനിച്ചത് നിരവധി തന്ത്രപരമായ പാഠങ്ങളാണ്. ആക്രമണ നിരയിലെ ഫ്ലൂയിഡിറ്റിയും മധ്യനിരയിലെ നിയന്ത്രണവും എതിരാളികളെ പ്രതിരോധത്തിലാക്കിയെങ്കിലും, പ്രതിരോധത്തിൽ ഇനിയും പരിഹരിക്കപ്പെടേണ്ട ചില കാര്യങ്ങൾ ഈ മത്സരം വ്യക്തമാക്കുന്നു. ഹാരിസ് നെന്മാറയുടെ സവിശേഷമായ വിശകലനം ഇവിടെ കാണാം.",
        "p2_en": "A detailed technical review of Real Madrid's tactical encounter with Italian side AS Roma. The analysis reviews positional interchangeability in Madrid's front line, penetration into the box, and areas of defensive concentration required ahead of major European tournaments.",
        "takeaways": [
            "Positional rotations between front-line attackers",
            "Box entries via progressive vertical passes",
            "Defensive transition balance against counter-attacking opponent pace",
            "Midfield tempo orchestration in controlling the match rhythm"
        ],
        "tags": ["Real Madrid", "AS Roma", "European Football", "Tactical Breakdown", "Haris Nenmara", "Football Analysis"]
    },
    {
        "id": "RtpY-aKasEg",
        "slug": "barcelona-vs-galatasaray-lamine-yamal-analysis",
        "sport": "football",
        "sport_title": "Football Analysis",
        "playlist": "Barcelona",
        "title": "ആളറിഞ്ഞു കളിക്കടാ ! barcelona vs galatasaray | lamine yamal | Haris Nenmara",
        "seo_title": "Barcelona vs Galatasaray Match Review | Lamine Yamal Focus | Final Third",
        "meta_desc": "Barcelona vs Galatasaray tactical match review in Malayalam. How Lamine Yamal and Barcelona broke down aggressive defensive setups with tactical flair.",
        "published_iso": "2026-10-19T10:00:00+00:00",
        "views": "72K views",
        "read_time": "3 min read",
        "p1_ml": "ബാഴ്സലോണയും ഗലാറ്റസരെയും തമ്മിൽ നടന്ന ആവേശകരമായ മത്സരത്തിന്റെ വിശകലനം. യൂറോപ്യൻ പോരാട്ടങ്ങളിൽ എതിരാളികളുടെ പ്രതിരോധ കോട്ടകൾ തകർക്കാൻ ബാഴ്സ സ്വീകരിച്ച അടവുകളും, കൗമാരതാരം ലാമിൻ യമാലിന്റെ വ്യക്തിഗത മികവും കളിയിൽ നിർണ്ണായകമായി. ഹാരിസ് നെന്മാറ പങ്കുവെക്കുന്ന തന്ത്രപരമായ നിരീക്ഷണങ്ങൾ.",
        "p2_en": "A tactical breakdown of Barcelona's clash against Galatasaray. We evaluate how Barcelona dismantled Galatasaray's defensive block using positional overloads, intelligent off-the-ball movements, and the individual genius of Lamine Yamal.",
        "takeaways": [
            "Breaking down aggressive low-block defensive structures",
            "Wing overloads creating isolation matchups in the final third",
            "Patience and ball retention against compact defensive teams",
            "Tactical maturity of young players on European nights"
        ],
        "tags": ["Barcelona", "Galatasaray", "Lamine Yamal", "European Football", "Haris Nenmara", "Final Third"]
    },
    {
        "id": "l1q1MQZSe_0",
        "slug": "kerala-blasters-sanan-momo-fitness-tactics",
        "sport": "football",
        "sport_title": "Football Analysis",
        "playlist": "Kerala Blasters & Indian Football",
        "title": "'സനാന് ഫിറ്റ്നസില്ല... മോമോയുടെ മെന്‍റാലിറ്റി'; ആഷ്‍ലിയുടെ തുറന്ന് പറച്ചിലുകള്‍ | Kerala blasters",
        "seo_title": "Kerala Blasters Squad Analysis: Sanan, Momo & Tactical Realities | Final Third",
        "meta_desc": "Kerala Blasters player fitness, tactical discipline, and mentality analyzed by Haris Nenmara. In-depth review of Sanan, Momo, and ISL campaign requirements.",
        "published_iso": "2026-10-18T14:30:00+00:00",
        "views": "55K views",
        "read_time": "3 min read",
        "p1_ml": "കേരള ബ്ലാസ്റ്റേഴ്സിന്റെ ഈ സീസണിലെ പ്രകടനങ്ങളെയും താരങ്ങളുടെ ഫിറ്റ്നസിനെയും സംബന്ധിച്ച് ആഷ്‌ലിയുടെ തുറന്നുപറച്ചിലുകൾ ചൂടേറിയ ചർച്ചകൾക്ക് വഴിവെച്ചിരിക്കുകയാണ്. സനാന്റെ ഫിറ്റ്നസ് പ്രശ്നങ്ങളും മോമോയുടെ കളിയിലെ മനോഭാവവും ടീമിന്റെ വിജയങ്ങളെ എങ്ങനെ ബാധിക്കുന്നുവെന്ന് ഹാരിസ് നെന്മാറ വസ്തുനിഷ്ഠമായി വിലയിരുത്തുന്നു. ബ്ലാസ്റ്റേഴ്സ് ആരാധകർ അറിഞ്ഞിരിക്കേണ്ട സുപ്രധാന വിവരങ്ങൾ.",
        "p2_en": "Kerala Blasters' campaign under the tactical microscope: scrutinizing squad fitness standards, pressing endurance, and mental resilience. Haris Nenmara evaluates the public commentary on Sanan's physical readiness and Momo's tactical role, explaining what the team must fix to maintain ISL competitiveness.",
        "takeaways": [
            "Impact of player physical conditioning on 90-minute pressing",
            "Momo's attacking positioning and pressing contribution",
            "Squad rotation challenges in long league tournaments",
            "Coaching decisions under pressure in the Indian Super League"
        ],
        "tags": ["Kerala Blasters", "KBFC", "ISL", "Indian Football", "Sanan", "Haris Nenmara"]
    },
    {
        "id": "ySpbZe77Jgs",
        "slug": "kerala-blasters-fallou-ndiaye-defensive-wall",
        "sport": "football",
        "sport_title": "Football Analysis",
        "playlist": "Kerala Blasters & Indian Football",
        "title": "ഫാലു ബാക്ക് ; ബ്ലാസ്റ്റേഴ്സ് ബാക്ക് ലൈൻ സുശക്തം | Fallou ndiaye| Kerala Blasters",
        "seo_title": "Fallou N'Diaye: Kerala Blasters Defensive Wall Analysis | Final Third",
        "meta_desc": "Can Fallou N'Diaye solidify Kerala Blasters' backline? Tactical analysis of his defensive positioning, aerial dominance, and ISL impact by Haris Nenmara.",
        "published_iso": "2026-10-15T08:00:00+00:00",
        "views": "35K views",
        "read_time": "3 min read",
        "p1_ml": "കേരള ബ്ലാസ്റ്റേഴ്സ് പ്രതിരോധ നിരയ്ക്ക് കരുത്തുപകരാൻ ഫാലു എൻദിയായെ തിരിച്ചെത്തുന്നു. അദ്ദേഹത്തിന്റെ വരവ് ബ്ലാസ്റ്റേഴ്സിന്റെ ബാക്ക്-ലൈനിന് എത്രത്തോളം ഉറപ്പ് നൽകും? ഏരിയൽ ഡ്യുവലുകളിലെ ആധിപത്യവും ടാക്കിളുകളിലെ കൃത്യതയും മഞ്ഞപ്പടയുടെ പ്രതിരോധപ്പിഴവുകൾ പരിഹരിക്കാൻ സഹായിക്കുമോ എന്ന് പരിശോധിക്കുന്ന സമഗ്രമായ വിശകലനം.",
        "p2_en": "Analyzing the return of Fallou N'Diaye to the Kerala Blasters defense. This video examines his aerial prowess, box-defending capabilities, and leadership qualities in stabilizing a backline that has faced high pressure in competitive ISL matches.",
        "takeaways": [
            "Dominance in aerial duels defending set pieces and long balls",
            "Interception positioning in a compact central defensive pairing",
            "Physicality and composure under opposition high press",
            "Leadership and communication across the back four"
        ],
        "tags": ["Kerala Blasters", "Fallou N'Diaye", "KBFC Defense", "ISL Tactics", "Haris Nenmara", "Indian Football"]
    },
    {
        "id": "cOYjZ39qHAU",
        "slug": "kerala-blasters-momo-yanson-attack-bolton-defense",
        "sport": "football",
        "sport_title": "Football Analysis",
        "playlist": "Kerala Blasters & Indian Football",
        "title": "അറ്റാക്കിൽ യാൻസൺ ; കോട്ട കാക്കാൻ ബോൾട്ടൻ | Kerala Blasters | Momo yansane | James Bolton",
        "seo_title": "Kerala Blasters Squad Analysis: Yansane in Attack, Bolton in Defense | Final Third",
        "meta_desc": "Kerala Blasters tactical balance: Momo Yansane leading the attack while James Bolton secures the defense. ISL squad analysis by Haris Nenmara.",
        "published_iso": "2026-10-14T11:00:00+00:00",
        "views": "48K views",
        "read_time": "3 min read",
        "p1_ml": "കേരള ബ്ലാസ്റ്റേഴ്സിന്റെ മുന്നേറ്റ നിരയിൽ മോമോ യാൻസണും പ്രതിരോധത്തിൽ ജെയിംസ് ബോൾട്ടനും ഒത്തുചേരുമ്പോൾ ടീമിന് ലഭിക്കുന്ന തന്ത്രപരമായ സന്തുലിതാവസ്ഥ എന്താണ്? അറ്റാക്കിങ്ങിലെ ഫിനിഷിങ് പോരായ്മകളും ഡിഫൻസിലെ വിടവുകളും പരിഹരിക്കാൻ ഇരുവരുടെയും സാനിധ്യം സഹായിക്കുമോ എന്ന് ഹാരിസ് നെന്മാറ വിശദീകരിക്കുന്നു.",
        "p2_en": "A strategic review of Kerala Blasters' spine: Momo Yansane's hold-up and pressing ability up front contrasted with James Bolton's defensive solidity at the back. This analysis breaks down how balancing both ends of the pitch creates tactical stability in the ISL.",
        "takeaways": [
            "Yansane's physical hold-up play linking attack with midfield",
            "James Bolton's positional discipline in defending the box",
            "Transition efficiency from defensive third to attacking third",
            "Overall squad balance required for consistent league points"
        ],
        "tags": ["Kerala Blasters", "Momo Yansane", "James Bolton", "ISL Analysis", "KBFC", "Haris Nenmara"]
    },
    {
        "id": "Ustsj3NHM4Y",
        "slug": "kerala-blasters-midfield-nebojsa-kosovic-tactics",
        "sport": "football",
        "sport_title": "Football Analysis",
        "playlist": "Kerala Blasters & Indian Football",
        "title": "ബ്ലാസ്റ്റേഴ്സ് മധ്യനിര ഇനി കൊസോവിച്ച് ഭരിക്കും | Kerala Blasters | Nebojša Kosović",
        "seo_title": "Nebojša Kosović: Kerala Blasters Midfield Maestro Analysis | Final Third",
        "meta_desc": "Can Nebojša Kosović control the midfield for Kerala Blasters? Tactical analysis of his passing range, vision, and midfield dictation by Haris Nenmara.",
        "published_iso": "2026-10-12T07:30:00+00:00",
        "views": "39K views",
        "read_time": "3 min read",
        "p1_ml": "കേരള ബ്ലാസ്റ്റേഴ്സ് മധ്യനിരയെ നിയന്ത്രിക്കാൻ എത്തിയ മോണ്ടിനെഗ്രോ താരം നെബോജ്സ കൊസോവിച്ചിന്റെ കളി ശൈലിയെക്കുറിച്ചുള്ള സമഗ്രമായ പഠനം. കളിയുടെ വേഗത നിയന്ത്രിക്കാനും കൃത്യമായ പാസുകളിലൂടെ മുന്നേറ്റ നിരയിലേക്ക് പന്തെത്തിക്കാനുമുള്ള അദ്ദേഹത്തിന്റെ കഴിവ് ബ്ലാസ്റ്റേഴ്സിന് എത്രത്തോളം മുതൽകൂട്ടാകുമെന്ന് ഹാരിസ് നെന്മാറ പരിശോധിക്കുന്നു.",
        "p2_en": "Evaluating the tactical profile of Nebojša Kosović at Kerala Blasters. We assess his passing range, vision under pressure, and how a true midfield controller can unlock defenses while protecting the center of the pitch in the ISL.",
        "takeaways": [
            "Vision and progressive passing between opponent defensive lines",
            "Tempo management and retaining possession under pressure",
            "Spatial positioning in central midfield transitions",
            "Set-piece delivery and creative chance generation"
        ],
        "tags": ["Kerala Blasters", "Nebojsa Kosovic", "KBFC Midfield", "ISL Tactics", "Haris Nenmara", "Indian Football"]
    },
    {
        "id": "ZuU9k-lVTzE",
        "slug": "kerala-blasters-aston-villa-green-new-signings",
        "sport": "football",
        "sport_title": "Football Analysis",
        "playlist": "Kerala Blasters & Indian Football",
        "title": "ആസ്റ്റൺ വില്ലയിൽ നിന്ന് കളി പഠിച്ച ഗ്രീൻ;കൊമ്പന്മാരുടെ പുതിയ സൈനിംഗുകൾ| Kerala Blasters New signings",
        "seo_title": "Kerala Blasters New Signings: Green & Squad Rebuilding | Final Third",
        "meta_desc": "Aston Villa academy graduate Green arrives at Kerala Blasters. Tactical breakdown of new signings and squad rebuilding by Haris Nenmara.",
        "published_iso": "2026-10-10T12:00:00+00:00",
        "views": "44K views",
        "read_time": "3 min read",
        "p1_ml": "പ്രീമിയർ ലീഗ് ക്ലബ്ബ് ആസ്റ്റൺ വില്ലയുടെ അക്കാദമിയിൽ നിന്ന് കളി പഠിച്ചെത്തിയ ഗ്രീനും ബ്ലാസ്റ്റേഴ്സിന്റെ പുതിയ സൈനിംഗുകളും ടീമിന് നൽകുന്ന പുതിയ പ്രതീക്ഷകൾ എന്തൊക്കെയാണ്? യുവതാരങ്ങളുടെ സാന്നിധ്യം മഞ്ഞപ്പടയുടെ കളി ശൈലിയിൽ വരുത്തുന്ന മാറ്റങ്ങൾ ഹാരിസ് നെന്മാറ വിശദീകരിക്കുന്നു.",
        "p2_en": "An overview of Kerala Blasters' latest recruitment strategy, spotlighting Aston Villa academy product Green. We evaluate how modern European youth football foundations can enhance Kerala Blasters' tactical intensity and squad depth in Indian football.",
        "takeaways": [
            "Technical fundamentals from top-tier European youth academies",
            "Versatility across wide and central attacking channels",
            "Impact of high-energy young signings on squad rotation",
            "Long-term rebuilding vision for the Kerala Blasters project"
        ],
        "tags": ["Kerala Blasters", "Green", "Aston Villa", "KBFC Signings", "ISL", "Haris Nenmara"]
    },
    {
        "id": "rNiXi4pW9nM",
        "slug": "lionel-messi-football-legacy-tactics",
        "sport": "football",
        "sport_title": "Football Analysis",
        "playlist": "2026 WORLDCUP Stories",
        "title": "ഇങ്ങനെ ഒരിതിഹാസം ഇനി പിറക്കുമോ ? Lionel Messi | Haris Nenmara",
        "seo_title": "Lionel Messi Tactical Legacy: Will We Ever See Another? | Final Third",
        "meta_desc": "A tribute to Lionel Messi's football genius. Haris Nenmara analyzes the spatial awareness, playmaking brilliance, and enduring legacy of the Argentine icon.",
        "published_iso": "2026-10-08T09:00:00+00:00",
        "views": "65K views",
        "read_time": "3 min read",
        "p1_ml": "ഫുട്ബോൾ ലോകത്ത് ലയണൽ മെസ്സിയെപ്പോലൊരു ഇതിഹാസം ഇനി വീണ്ടും പിറക്കുമോ? കളിക്കളത്തിൽ ഇടങ്ങൾ കണ്ടെത്തുന്നതിലും കളിയുടെ ഗതി ഒറ്റയ്ക്ക് മാറ്റുന്നതിലും മെസ്സി കാണിച്ച പ്രതിഭ അദ്വിതീയമാണ്. കരിയറിന്റെ വിവിധ ഘട്ടങ്ങളിൽ മെസ്സി തന്റെ കളി ശൈലി എങ്ങനെ മാറ്റിമറിച്ചുവെന്നും ഫുട്ബോൾ ചരിത്രത്തിൽ അദ്ദേഹത്തിന്റെ സ്ഥാനം എന്താണെന്നും ഹാരിസ് നെന്മാറ ഹൃദയസ്പർശിയായി വിശകലനം ചെയ്യുന്നു.",
        "p2_en": "Reflecting on the incomparable tactical and creative genius of Lionel Messi. Haris Nenmara explores Messi's extraordinary spatial intelligence, walking play style that reads opponent spacing, and how his transition from explosive winger to supreme playmaker redefined modern football.",
        "takeaways": [
            "Spatial scanning and reading defensive structural weaknesses",
            "Evolution from rapid dribbler to master orchestral playmaker",
            "Decisive playmaking in championship and World Cup moments",
            "The enduring legacy of football's greatest number ten"
        ],
        "tags": ["Lionel Messi", "Messi Analysis", "World Cup", "Football Legends", "Haris Nenmara", "Final Third"]
    },
    {
        "id": "mVR_mRYU2YE",
        "slug": "cristiano-ronaldo-cr7-tactical-philosophy",
        "sport": "football",
        "sport_title": "Football Analysis",
        "playlist": "2026 WORLDCUP Stories",
        "title": "കോച്ചോ റോണോയോ; ആരാണ് ശരി? | Cristiano Ronaldo | Ronaldo Walkout | CR7",
        "seo_title": "Cristiano Ronaldo vs Management: Who Was Right? CR7 Analysis | Final Third",
        "meta_desc": "Coach vs Cristiano Ronaldo: who was right? Haris Nenmara investigates the tactical and psychological clash surrounding the CR7 walkout and modern football demands.",
        "published_iso": "2026-10-05T14:00:00+00:00",
        "views": "108K views",
        "read_time": "3 min read",
        "p1_ml": "മാഞ്ചസ്റ്റർ യുണൈറ്റഡിലും പോർച്ചുഗൽ ദേശീയ ടീമിലും ക്രിസ്റ്റ്യാനോ റൊണാൾഡോയും പരിശീലകരും തമ്മിലുണ്ടായ അഭിപ്രായവ്യത്യാസങ്ങളുടെ ആഴത്തിലുള്ള പരിശോധന. പ്രശസ്തമായ വാക്ക്ഔട്ട് സംഭവത്തിന് പിന്നിലെ യഥാർത്ഥ കാരണങ്ങളെന്തായിരുന്നു? ആധുനിക ഫുട്ബോളിലെ ഉയർന്ന പ്രസ്സിങ് ഡിമാൻഡുകളും റൊണാൾഡോ എന്ന എലൈറ്റ് ഗോൾവേട്ടക്കാരന്റെ റോളും തമ്മിലുള്ള സംഘർഷത്തെ ഹാരിസ് നെന്മാറ വിശകലനം ചെയ്യുന്നു.",
        "p2_en": "Analyzing the tactical and leadership tension between superstar Cristiano Ronaldo and modern manager systems. Haris Nenmara weighs both perspectives: the demanding tactical pressing requirements of modern football versus utilizing the greatest goalscorer of a generation.",
        "takeaways": [
            "Tactical balance between team pressing systems and individual finishing",
            "Managing elite superstar personalities in high-pressure clubs",
            "The evolution of the striker role in contemporary football",
            "Ronaldo's unmatched professionalism and hunger for victory"
        ],
        "tags": ["Cristiano Ronaldo", "CR7", "Manchester United", "Football Tactics", "Ronaldo Walkout", "Haris Nenmara"]
    },

    # ========================== CRICKET (6) ==========================
    {
        "id": "qDn--g-xzQY",
        "slug": "abhishek-sharma-vaibhav-suryavanshi-ind-vs-nz",
        "sport": "cricket",
        "sport_title": "Cricket Analysis",
        "playlist": "Cricket Stories & Analysis",
        "title": "ബ്രൂട്ടൽ; അഭിഷേകും വൈഭവും ചേർന്ന് കിവികളെ കുഴിച്ച് മൂടി | Abhishek Sharma | Vaibhav Suryavanshi",
        "seo_title": "Brutal Attack: Abhishek Sharma & Vaibhav Suryavanshi Demolish NZ | Final Third",
        "meta_desc": "Fearless T20 batting: Abhishek Sharma and young sensation Vaibhav Suryavanshi dismantle New Zealand bowling. Match debrief by Haris Nenmara.",
        "published_iso": "2026-10-25T14:00:00+00:00",
        "views": "281K views",
        "read_time": "3 min read",
        "p1_ml": "ന്യൂസിലൻഡിനെതിരെ ഇന്ത്യൻ ബാറ്റിങ് നിര കെട്ടഴിച്ചുവിട്ട ബാറ്റിങ് വെടിക്കെട്ടിന്റെ പൂർണ്ണ വിവരങ്ങൾ. അഭിഷേക് ശർമ്മയുടെ തകർപ്പൻ ബാറ്റിങ്ങും കൗമാരതാരം വൈഭവ് സൂര്യവംശിയുടെ ഭയമില്ലാത്ത സമീപനവും കിവി ബോളിങ് നിരയെ നിഷ്പ്രഭമാക്കി. ഇന്ത്യൻ ക്രിക്കറ്റിന്റെ ഭാവി ബാറ്റിങ് ശൈലിയെക്കുറിച്ച് ഹാരിസ് നെന്മാറ പങ്കുവെക്കുന്ന നിരീക്ഷണങ്ങൾ.",
        "p2_en": "An explosive review of India's destructive powerplay batting against New Zealand. Haris Nenmara analyzes the aggressive mindset of Abhishek Sharma and rising sensation Vaibhav Suryavanshi, breaking down how fearless intent and modern bat swings dismantled New Zealand's bowling attack.",
        "takeaways": [
            "Fearless intent and intent-first approach in modern powerplays",
            "Dominance against both pace and spin from ball one",
            "Emergence of Vaibhav Suryavanshi as an elite young talent",
            "The evolving blueprint of Team India's aggressive T20 batting"
        ],
        "tags": ["Abhishek Sharma", "Vaibhav Suryavanshi", "Ind vs NZ", "Cricket Analysis", "T20 Cricket", "Haris Nenmara"]
    },
    {
        "id": "Xq1PtXOrVRc",
        "slug": "sanju-samson-redemption-story-india-vs-nz",
        "sport": "cricket",
        "sport_title": "Cricket Analysis",
        "playlist": "Cricket Stories & Analysis",
        "title": "സഞ്ജുവിൻ്റെ പ്രതികാര കഥ തുടരുന്നു ! Sanju Samson | India vs Newzealand",
        "seo_title": "Sanju Samson Redemption Story Continues: India vs NZ Analysis | Final Third",
        "meta_desc": "Sanju Samson's incredible comeback story against New Zealand. Technical adjustments, mental strength, and match-winning knocks evaluated by Haris Nenmara.",
        "published_iso": "2026-10-24T18:00:00+00:00",
        "views": "175K views",
        "read_time": "3 min read",
        "p1_ml": "വിമർശകർക്ക് ബാറ്റുകൊണ്ട് മറുപടി നൽകി സഞ്ജു സാംസൺ തന്റെ പ്രതാപം വീണ്ടെടുക്കുകയാണ്. ന്യൂസിലൻഡിനെതിരായ മത്സരത്തിൽ സഞ്ജു പുറത്തെടുത്ത പക്വതയാർന്ന പ്രകടനവും അദ്ദേഹത്തിന്റെ കളിയിലെ സാങ്കേതിക മാറ്റങ്ങളും ഹാരിസ് നെന്മാറ വിശദീകരിക്കുന്നു. സഞ്ജുവിന്റെ യാത്രയിലെ ഈ വഴിത്തിരിവ് ഇന്ത്യൻ ക്രിക്കറ്റിൽ അദ്ദേഹത്തിന്റെ സ്ഥാനത്തെ എങ്ങനെ ഉറപ്പിക്കുമെന്ന് ഈ വീഡിയോ വ്യക്തമാക്കുന്നു.",
        "p2_en": "Sanju Samson's inspiring journey of redemption against New Zealand analyzed in detail. Haris Nenmara evaluates Samson's technical improvements at the crease, improved shot selection against pace, and the calm mental fortitude that delivered under the national spotlight.",
        "takeaways": [
            "Technical adjustments against deliveries aimed at the body",
            "Patience in shot selection during the initial overs of the innings",
            "Mental resilience in handling intense media and selection scrutiny",
            "Cementing a core top-order role in Team India's white-ball plans"
        ],
        "tags": ["Sanju Samson", "Ind vs NZ", "Team India", "Cricket Comeback", "Haris Nenmara", "Final Third"]
    },
    {
        "id": "I-40yws8G-E",
        "slug": "sanju-samson-ind-vs-nz-match-answers",
        "sport": "cricket",
        "sport_title": "Cricket Analysis",
        "playlist": "Cricket Stories & Analysis",
        "title": "സഞ്ജുവിൻ്റെ മറുപടികൾ കൊള്ളുന്നത് ആർക്കാണ് ? Sanju Samson | Ind Vs Nz",
        "seo_title": "Sanju Samson's Statement Knock: Answers on the Field | Final Third",
        "meta_desc": "Who does Sanju Samson's innings answer? Tactical analysis of his high-pressure match performance against New Zealand by Haris Nenmara.",
        "published_iso": "2026-10-23T16:00:00+00:00",
        "views": "85K views",
        "read_time": "3 min read",
        "p1_ml": "സഞ്ജു സാംസണിന്റെ മികച്ച പ്രകടനങ്ങൾ കളിക്കളത്തിന് പുറത്തുള്ള ആർക്കൊക്കെയാണ് മറുപടിയാകുന്നത്? അവസരങ്ങൾ കുറവായിരുന്നിട്ടും ലഭിച്ച അവസരങ്ങളിൽ ടീമിനായി തകർപ്പൻ പ്രകടനം പുറത്തെടുക്കുന്ന സഞ്ജുവിന്റെ പോരാട്ടവീര്യത്തെ ഹാരിസ് നെന്മാറ വിശകലനം ചെയ്യുന്നു. ഇന്ത്യൻ ടീം മാനേജ്മെന്റിന്റെ തീരുമാനങ്ങളും ടീം ബാലൻസും ഇതിൽ ചർച്ചയാകുന്നു.",
        "p2_en": "A tactical and contextual review of Sanju Samson's decisive answers on the cricket pitch. Haris Nenmara breaks down how Samson's match-winning contributions overcome continuous selection debates and provide the wicket-keeping batsman balance India needs.",
        "takeaways": [
            "Handling extreme pressure with aggressive clarity of thought",
            "Dual role impact: clean glovework and rapid run generation",
            "Tactical balance provided to India's middle and top order",
            "Consistency across varying match conditions and bowling attacks"
        ],
        "tags": ["Sanju Samson", "Ind vs NZ", "Indian Cricket", "Cricket Selection", "Haris Nenmara", "Final Third"]
    },
    {
        "id": "F1X3eE_CBKU",
        "slug": "tilak-varma-naman-dhir-comeback-analysis",
        "sport": "cricket",
        "sport_title": "Cricket Analysis",
        "playlist": "Cricket Stories & Analysis",
        "title": "ഇതൊക്കെയാണ് കംബാക്ക് ! നമൻ ധീർ പ്രതീക്ഷയാണ് | Tilak Varma | NamanDhir",
        "seo_title": "Tilak Varma Comeback & Naman Dhir Rising Star Analysis | Final Third",
        "meta_desc": "Tilak Varma's sensational comeback and Naman Dhir's emergence as an explosive batting talent analyzed in Malayalam by Haris Nenmara.",
        "published_iso": "2026-10-20T17:00:00+00:00",
        "views": "57K views",
        "read_time": "3 min read",
        "p1_ml": "തിലക് വർമ്മയുടെ ഗംഭീര തിരിച്ചുവരവും യുവതാരം നമൻ ധീറിന്റെ വിസ്മയിപ്പിക്കുന്ന ബാറ്റിങ് പ്രകടനവും ഇന്ത്യൻ ക്രിക്കറ്റിന് നൽകുന്ന വലിയ ശുഭസൂചനകൾ എന്തൊക്കെയാണ്? പ്രതിസന്ധി ഘട്ടങ്ങളിൽ ഇന്നിങ്സ് മുന്നോട്ട് നയിക്കാനുള്ള തിലകിന്റെ കഴിവും നമൻ ധീറിന്റെ കൂറ്റൻ സിക്സറുകളും ഹാരിസ് നെന്മാറ വിശദമായി വിലയിരുത്തുന്നു.",
        "p2_en": "Analyzing the tactical poise of Tilak Varma's comeback alongside the dynamic emergence of Naman Dhir. Haris Nenmara examines middle-order temperament, accelerating under pressure, and how these young batters fit into India's long-term white-ball strategy.",
        "takeaways": [
            "Tilak Varma's composure in anchoring and accelerating innings",
            "Naman Dhir's raw power and boundary-hitting prowess",
            "Left-hand right-hand combinations disorienting bowling plans",
            "The bright future of young Indian white-ball batting talent"
        ],
        "tags": ["Tilak Varma", "Naman Dhir", "Team India", "Cricket Comeback", "T20 Cricket", "Haris Nenmara"]
    },
    {
        "id": "3-k7z6FqTX0",
        "slug": "jasprit-bumrah-sanju-samson-ind-vs-wi",
        "sport": "cricket",
        "sport_title": "Cricket Analysis",
        "playlist": "Cricket India",
        "title": "ഭുവി വരുന്നു ! ബുംറ ഇല്ലെങ്കിൽ ഇന്ത്യ ഇല്ലേ ? Sanju Samson | Jasprit Bumrah |Ind Vs Wi",
        "seo_title": "Is India Dependent on Bumrah? Bhuvneshwar & Samson Debrief | Final Third",
        "meta_desc": "Is India overly reliant on Jasprit Bumrah? Fast bowling tactics, Bhuvneshwar Kumar, and Sanju Samson discussed by Haris Nenmara.",
        "published_iso": "2026-10-16T11:30:27+00:00",
        "views": "110K views",
        "read_time": "3 min read",
        "p1_ml": "ജസ്പ്രീത് ബുംറ എന്ന ഇതിഹാസ പേസറുടെ അസാന്നിധ്യത്തിൽ ഇന്ത്യൻ ബോളിങ് നിര നേരിടുന്ന വെല്ലുവിളികൾ പരിശോധിക്കുന്ന വീഡിയോ. ഭുവനേശ്വർ കുമാറിന്റെ സ്വിങ് ബോളിങ്ങും പരിചയസമ്പത്തും ഇന്ത്യൻ ടീമിന് എത്രത്തോളം ആവശ്യമാണ്? ഡെത്ത് ഓവറുകളിലെ റൺ ഒഴുക്ക് തടയാൻ ബുംറയെപ്പോലൊരു ബൗളറുടെ വിടവ് എങ്ങനെ നികത്താം എന്ന ചോദ്യത്തിന് ഹാരിസ് നെന്മാറ തന്ത്രപരമായ മറുപടികൾ നൽകുന്നു.",
        "p2_en": "Analyzing Team India's fast-bowling depth and reliance on Jasprit Bumrah. We evaluate powerplay swing from Bhuvneshwar Kumar, death-over yorker execution, and how different bowling combinations perform under pressure against aggressive batting lineups.",
        "takeaways": [
            "Jasprit Bumrah's unmatched wicket-taking threat across all phases",
            "The tactical value of Bhuvneshwar Kumar's new-ball swing control",
            "Death-over bowling execution and slower ball variations",
            "Strategic pace bowling combinations for international tournaments"
        ],
        "tags": ["Jasprit Bumrah", "Bhuvneshwar Kumar", "Sanju Samson", "Indian Bowling", "Cricket Tactics", "Haris Nenmara"]
    },
    {
        "id": "znjseVIMsE0",
        "slug": "bhuvneshwar-kumar-jasprit-bumrah-bowling-tactics",
        "sport": "cricket",
        "sport_title": "Cricket Analysis",
        "playlist": "Cricket India",
        "title": "ഭുവിയും ബുംറയും ചേർന്നാൽ ! Bhuvneshwar Kumar | Jasprit Bumrah",
        "seo_title": "Bhuvi + Bumrah: The Deadly Bowling Partnership | Final Third",
        "meta_desc": "The lethal bowling partnership: Bhuvneshwar Kumar and Jasprit Bumrah. Powerplay swing meets death-over yorkers. Analysis by Haris Nenmara.",
        "published_iso": "2026-10-17T11:36:23+00:00",
        "views": "21K views",
        "read_time": "3 min read",
        "p1_ml": "ഭുവനേശ്വർ കുമാറിന്റെ കൃത്യതയാർന്ന ന്യൂ-ബോൾ സ്വിംഗും ജസ്പ്രീത് ബുംറയുടെ മാരകമായ യോർക്കറുകളും ഒന്നിച്ചപ്പോൾ ഇന്ത്യൻ ക്രിക്കറ്റ് ആസ്വദിച്ചത് ചരിത്രത്തിലെ ഏറ്റവും മികച്ച ബോളിങ് കൂട്ടുകെട്ടുകളിലൊന്നാണ്. ബാറ്റ്സ്മാൻമാരെ എങ്ങനെയാണ് ഇവർ സമ്മർദ്ദത്തിലാക്കുന്നതെന്നും, രണ്ട് വ്യത്യസ്ത ശൈലികൾ പരസ്പരം പൂരകമായി മാറുന്നത് എങ്ങനെയെന്നും വിശദീകരിക്കുന്ന തന്ത്രപരമായ വീഡിയോ.",
        "p2_en": "A masterclass in bowling synergy: Bhuvneshwar Kumar's swing mastery paired with Jasprit Bumrah's raw pace and yorker accuracy. This debrief studies dot-ball pressure, partnership bowling, and why complementary styles are essential for winning tournaments.",
        "takeaways": [
            "Complementary bowling styles dismantling opening batting combinations",
            "Dot-ball pressure from one end creating wicket chances at the other",
            "Mastery of swing in the powerplay and pinpoint accuracy at the death",
            "Strategic blueprint for iconic fast-bowling partnerships"
        ],
        "tags": ["Bhuvneshwar Kumar", "Jasprit Bumrah", "Pace Bowling", "Cricket Partnerships", "India Cricket", "Final Third"]
    }
]

# Generate common navigation header
def render_navbar(active_page=""):
    football_active = ' active' if active_page == 'football' else ''
    cricket_active = ' active' if active_page == 'cricket' else ''
    home_active = ' active' if active_page == 'home' else ''
    
    return f"""  <header class="site-header">
    <div class="nav-container">
      <a href="/" class="brand-link" aria-label="Final Third Home">
        <picture>
          <source srcset="/assets/images/final-third-logo.webp" type="image/webp">
          <img src="/assets/images/final-third-logo.png" alt="Final Third Logo" class="brand-logo" width="160" height="36">
        </picture>
        <span class="brand-name">FINAL THIRD</span>
      </a>

      <!-- Desktop Navigation Links -->
      <nav class="main-nav" aria-label="Main Navigation">
        <ul class="nav-list">
          <li><a href="/" class="nav-link{home_active}">Home</a></li>
          <li><a href="/football/" class="nav-link{football_active}">⚽ Football Hub</a></li>
          <li><a href="/cricket/" class="nav-link{cricket_active}">🏏 Cricket Hub</a></li>
          <li><a href="/#videos" class="nav-link">Full Catalog (300+)</a></li>
          <li><a href="/#about" class="nav-link">About Haris</a></li>
          <li><a href="/#contact" class="nav-link">Contact</a></li>
        </ul>
      </nav>

      <!-- Action Buttons -->
      <div class="nav-actions">
        <a href="https://www.youtube.com/@FinalThird_HarisNenmara" target="_blank" rel="noopener noreferrer" class="btn btn-subscribe" aria-label="Subscribe on YouTube">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
            <path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>
          </svg>
          SUBSCRIBE
        </a>
        <button class="mobile-toggle" id="mobileMenuToggle" aria-label="Toggle Navigation Menu" aria-expanded="false">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16m-7 6h7" />
          </svg>
        </button>
      </div>
    </div>
  </header>

  <!-- Mobile Drawer -->
  <div class="mobile-drawer" id="mobileDrawer" aria-hidden="true">
    <div class="drawer-content">
      <ul class="drawer-list">
        <li><a href="/" class="drawer-link{home_active}">Home</a></li>
        <li><a href="/football/" class="drawer-link{football_active}">⚽ Football Category Hub (14 Videos)</a></li>
        <li><a href="/cricket/" class="drawer-link{cricket_active}">🏏 Cricket Category Hub (6 Videos)</a></li>
        <li><a href="/#videos" class="drawer-link">Full Video Catalog (300+)</a></li>
        <li><a href="/#about" class="drawer-link">About Haris Nenmara</a></li>
        <li><a href="/privacy.html" class="drawer-link">Privacy Policy</a></li>
        <li><a href="/#contact" class="drawer-link">Contact &amp; Sponsorships</a></li>
      </ul>
      <div style="margin-top: 1.5rem; padding-top: 1rem; border-top: 1px solid #2a2a2a;">
        <a href="https://www.youtube.com/@FinalThird_HarisNenmara" target="_blank" rel="noopener noreferrer" class="btn btn-subscribe" style="width: 100%; justify-content: center;">
          SUBSCRIBE ON YOUTUBE ↗
        </a>
      </div>
    </div>
  </div>"""

# Render individual video page
def render_page(video):
    vid = video["id"]
    slug = video["slug"]
    sport = video["sport"]
    sport_name = "Football" if sport == "football" else "Cricket"
    sport_hub_url = f"/{sport}/"
    url = f"{DOMAIN}/{sport}/{slug}/"
    thumb_hq = f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg"
    thumb_max = f"https://i.ytimg.com/vi/{vid}/maxresdefault.jpg"
    
    # 4 Related videos from the same sport
    same_sport_videos = [v for v in VIDEOS if v["sport"] == sport and v["id"] != vid]
    related = same_sport_videos[:4]
    if len(related) < 4:
        other_videos = [v for v in VIDEOS if v["id"] != vid and v not in related]
        related += other_videos[:4 - len(related)]
    
    related_cards_html = ""
    for r in related:
        r_url = f"/{r['sport']}/{r['slug']}/"
        related_cards_html += f"""
        <article class="related-card" onclick="window.location.href='{r_url}'" style="cursor: pointer;">
          <a href="{r_url}" class="related-thumb-link" aria-label="{r['title']}">
            <img src="https://i.ytimg.com/vi/{r['id']}/hqdefault.jpg" alt="{r['title']}" width="320" height="180" loading="lazy" decoding="async">
            <span class="related-sport-pill">{r['sport'].upper()}</span>
          </a>
          <div class="related-info">
            <span class="related-meta">{r['playlist']} · {r['views']}</span>
            <h4 class="related-title"><a href="{r_url}">{r['title']}</a></h4>
            <a href="{r_url}" class="related-action-link">Read Breakdown ↗</a>
          </div>
        </article>"""

    takeaways_html = "".join([f"<li>{t}</li>" for t in video["takeaways"]])
    tags_html = "".join([f'<span class="tag-pill">#{t}</span>' for t in video["tags"]])

    html = f"""<!DOCTYPE html>
<html lang="en" xml:lang="ml" dir="ltr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{video['seo_title']}</title>
  <meta name="description" content="{video['meta_desc']}">
  <meta name="author" content="Haris Nenmara (ഹാരിസ് നെന്മാറ)">
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
  <link rel="canonical" href="{url}">

  <!-- Favicon -->
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/images/favicon-32x32.png">

  <!-- Open Graph -->
  <meta property="og:site_name" content="Final Third with Haris Nenmara">
  <meta property="og:type" content="video.other">
  <meta property="og:url" content="{url}">
  <meta property="og:title" content="{video['seo_title']}">
  <meta property="og:description" content="{video['meta_desc']}">
  <meta property="og:image" content="{thumb_max}">
  <meta property="og:image:alt" content="{video['title']}">
  <meta property="og:locale" content="ml_IN">
  <meta property="og:locale:alternate" content="en_IN">

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{video['seo_title']}">
  <meta name="twitter:description" content="{video['meta_desc']}">
  <meta name="twitter:image" content="{thumb_max}">

  <!-- Tracking -->
  <script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
  new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
  j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
  'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
  }})(window,document,'script','dataLayer','GTM-KFC9JGQJ');</script>

  <script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
  new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
  j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
  'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
  }})(window,document,'script','dataLayer','GTM-5N6XFRJ7');</script>

  <script async src="https://www.googletagmanager.com/gtag/js?id=G-XR8PCQNHRE"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-XR8PCQNHRE');
  </script>

  <!-- Google AdSense -->
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5399554232098923" crossorigin="anonymous"></script>

  <!-- Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Anek+Malayalam:wght@400;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">

  <!-- Schema.org JSON-LD -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@graph": [
      {{
        "@type": "VideoObject",
        "@id": "{url}#video",
        "name": {json.dumps(video['title'], ensure_ascii=False)},
        "description": {json.dumps(video['meta_desc'], ensure_ascii=False)},
        "thumbnailUrl": [
          "{thumb_max}",
          "{thumb_hq}"
        ],
        "uploadDate": "{video['published_iso']}",
        "embedUrl": "https://www.youtube.com/embed/{vid}",
        "contentUrl": "https://www.youtube.com/watch?v={vid}",
        "inLanguage": "ml",
        "creator": {{
          "@type": "Person",
          "@id": "{DOMAIN}/#person",
          "name": "Haris Nenmara",
          "alternateName": "ഹാരിസ് നെന്മാറ",
          "jobTitle": "Sports Journalist & Analyst"
        }},
        "publisher": {{
          "@type": "SportsOrganization",
          "@id": "{DOMAIN}/#organization",
          "name": "Final Third",
          "url": "{DOMAIN}/"
        }}
      }},
      {{
        "@type": "BreadcrumbList",
        "@id": "{url}#breadcrumb",
        "itemListElement": [
          {{
            "@type": "ListItem",
            "position": 1,
            "name": "Home",
            "item": "{DOMAIN}/"
          }},
          {{
            "@type": "ListItem",
            "position": 2,
            "name": "{sport_name} Analysis",
            "item": "{DOMAIN}{sport_hub_url}"
          }},
          {{
            "@type": "ListItem",
            "position": 3,
            "name": {json.dumps(video['title'], ensure_ascii=False)},
            "item": "{url}"
          }}
        ]
      }},
      {{
        "@type": "WebPage",
        "@id": "{url}#webpage",
        "url": "{url}",
        "name": {json.dumps(video['seo_title'], ensure_ascii=False)},
        "isPartOf": {{
          "@id": "{DOMAIN}/#website"
        }},
        "primaryImageOfPage": "{thumb_max}"
      }}
    ]
  }}
  </script>

  <style>
    :root {{
      --neon-lime: #9EE20B;
      --neon-lime-hover: #b4f51e;
      --pitch-black: #080808;
      --charcoal: #151515;
      --charcoal-light: #202020;
      --charcoal-border: #2a2a2a;
      --off-white: #F5F5F0;
      --muted-grey: #a0a0a0;
      --dark-grey: #666666;
      --font-primary: 'Anek Malayalam', 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background-color: var(--pitch-black);
      color: var(--off-white);
      font-family: var(--font-primary);
      line-height: 1.7;
      font-size: 1rem;
      -webkit-font-smoothing: antialiased;
    }}

    a {{ color: var(--neon-lime); text-decoration: none; transition: color 0.2s ease; }}
    a:hover {{ color: var(--neon-lime-hover); text-decoration: underline; }}

    /* Header & Navigation */
    .site-header {{
      border-bottom: 1px solid var(--charcoal-border);
      background-color: rgba(8, 8, 8, 0.95);
      backdrop-filter: blur(10px);
      position: sticky;
      top: 0;
      z-index: 100;
      padding: 0.875rem 1.5rem;
    }}
    .nav-container {{
      max-width: 1140px;
      margin: 0 auto;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .brand-link {{
      display: flex;
      align-items: center;
      gap: 0.75rem;
      color: var(--off-white);
      font-weight: 800;
      font-size: 1.125rem;
      letter-spacing: -0.02em;
    }}
    .brand-logo {{ height: 36px; width: auto; display: block; }}
    .brand-name {{ font-weight: 800; color: var(--off-white); letter-spacing: -0.02em; }}
    .main-nav {{ display: flex; align-items: center; }}
    .nav-list {{ display: flex; align-items: center; gap: 1.5rem; list-style: none; }}
    .nav-link {{ color: var(--muted-grey); font-weight: 600; font-size: 0.875rem; transition: color 0.2s; }}
    .nav-link:hover, .nav-link.active {{ color: var(--neon-lime); text-decoration: none; }}
    .nav-actions {{ display: flex; align-items: center; gap: 1rem; }}
    .btn-subscribe {{
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
      padding: 0.5rem 1rem;
      background: var(--neon-lime);
      color: #000;
      font-weight: 800;
      font-size: 0.8125rem;
      border-radius: 6px;
      text-decoration: none;
      transition: background-color 0.2s;
    }}
    .btn-subscribe:hover {{ background: var(--neon-lime-hover); text-decoration: none; }}
    .mobile-toggle {{
      display: none;
      background: none;
      border: none;
      color: var(--off-white);
      cursor: pointer;
    }}
    .mobile-drawer {{
      display: none;
      background: var(--charcoal);
      border-bottom: 1px solid var(--charcoal-border);
      padding: 1.5rem;
    }}
    .mobile-drawer.open {{ display: block; }}
    .drawer-list {{ list-style: none; display: flex; flex-direction: column; gap: 1rem; }}
    .drawer-link {{ color: var(--off-white); font-weight: 600; font-size: 1rem; text-decoration: none; }}
    .drawer-link.active {{ color: var(--neon-lime); }}

    /* Breadcrumbs Bar */
    .breadcrumb-bar {{
      max-width: 1140px;
      margin: 1.25rem auto 0;
      padding: 0 1.5rem;
      font-size: 0.8125rem;
      color: var(--dark-grey);
      display: flex;
      align-items: center;
      gap: 0.5rem;
      flex-wrap: wrap;
    }}
    .breadcrumb-bar a {{ color: var(--muted-grey); }}
    .breadcrumb-bar a:hover {{ color: var(--neon-lime); }}
    .breadcrumb-sep {{ color: var(--dark-grey); font-weight: 700; }}
    .breadcrumb-current {{
      color: var(--off-white);
      font-weight: 600;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      max-width: 500px;
    }}

    /* Back Link Bar */
    .back-link-bar {{
      max-width: 1140px;
      margin: 0.75rem auto 0;
      padding: 0 1.5rem;
    }}
    .back-link {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 0.8125rem;
      font-weight: 700;
      color: var(--neon-lime);
      text-decoration: none;
      transition: transform 0.2s;
    }}
    .back-link:hover {{ text-decoration: underline; transform: translateX(-3px); }}

    /* Layout */
    .page-layout {{
      max-width: 1140px;
      margin: 1rem auto 5rem;
      padding: 0 1.5rem;
      display: grid;
      grid-template-columns: 1fr 340px;
      gap: 2.5rem;
    }}

    /* Video Hero Box */
    .video-hero {{
      background: var(--charcoal);
      border: 1px solid var(--charcoal-border);
      border-radius: 12px;
      overflow: hidden;
      margin-bottom: 2rem;
    }}
    .video-aspect-frame {{
      position: relative;
      width: 100%;
      padding-top: 56.25%;
      background: #000;
    }}
    .video-aspect-frame iframe {{
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      border: 0;
    }}
    .video-meta-bar {{
      padding: 1.5rem;
      border-bottom: 1px solid var(--charcoal-border);
    }}
    .meta-pills {{
      display: flex;
      align-items: center;
      gap: 0.75rem;
      margin-bottom: 0.75rem;
      flex-wrap: wrap;
    }}
    .sport-pill {{
      background-color: var(--neon-lime);
      color: #000;
      font-size: 0.75rem;
      font-weight: 800;
      padding: 0.2rem 0.6rem;
      border-radius: 4px;
      letter-spacing: 0.05em;
    }}
    .playlist-pill {{
      background-color: var(--charcoal-light);
      border: 1px solid var(--charcoal-border);
      color: var(--muted-grey);
      font-size: 0.75rem;
      font-weight: 600;
      padding: 0.2rem 0.6rem;
      border-radius: 4px;
    }}
    .views-pill {{
      color: var(--muted-grey);
      font-size: 0.8125rem;
      font-weight: 600;
      display: flex;
      align-items: center;
      gap: 4px;
    }}
    .article-h1 {{
      font-size: 1.75rem;
      font-weight: 800;
      line-height: 1.35;
      color: var(--off-white);
      margin-bottom: 1rem;
    }}
    .cta-row {{
      display: flex;
      gap: 0.75rem;
      flex-wrap: wrap;
      margin-top: 1.25rem;
    }}

    .btn {{
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
      padding: 0.625rem 1.25rem;
      border-radius: 6px;
      font-weight: 700;
      font-size: 0.875rem;
      text-decoration: none;
      transition: all 0.2s ease;
    }}
    .btn-primary {{
      background-color: var(--neon-lime);
      color: #000;
    }}
    .btn-primary:hover {{
      background-color: var(--neon-lime-hover);
      text-decoration: none;
      transform: translateY(-1px);
    }}
    .btn-outline {{
      background: transparent;
      border: 1px solid var(--charcoal-border);
      color: var(--off-white);
    }}
    .btn-outline:hover {{
      border-color: var(--neon-lime);
      color: var(--neon-lime);
      text-decoration: none;
    }}

    /* Editorial Section */
    .editorial-content {{
      background: var(--charcoal);
      border: 1px solid var(--charcoal-border);
      border-radius: 12px;
      padding: 2rem;
      margin-bottom: 2rem;
    }}
    .editorial-content h2 {{
      font-size: 1.25rem;
      font-weight: 700;
      color: var(--neon-lime);
      margin-bottom: 1rem;
      letter-spacing: -0.01em;
    }}
    .editorial-content p {{
      color: #d8d8d8;
      font-size: 1.0625rem;
      margin-bottom: 1.25rem;
      line-height: 1.8;
    }}
    .takeaways-box {{
      background-color: rgba(158, 226, 11, 0.05);
      border-left: 3px solid var(--neon-lime);
      padding: 1.25rem 1.5rem;
      border-radius: 0 8px 8px 0;
      margin: 1.5rem 0;
    }}
    .takeaways-box h3 {{
      font-size: 1rem;
      font-weight: 800;
      color: var(--off-white);
      margin-bottom: 0.75rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }}
    .takeaways-box ul {{ list-style-type: none; }}
    .takeaways-box ul li {{
      position: relative;
      padding-left: 1.5rem;
      margin-bottom: 0.5rem;
      font-size: 0.9375rem;
      color: #e5e5e5;
    }}
    .takeaways-box ul li::before {{
      content: "✔";
      position: absolute;
      left: 0;
      color: var(--neon-lime);
      font-weight: 800;
    }}
    .tags-row {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.5rem;
      margin-top: 1.5rem;
      padding-top: 1rem;
      border-top: 1px solid var(--charcoal-border);
    }}
    .tag-pill {{
      background: var(--charcoal-light);
      border: 1px solid var(--charcoal-border);
      color: var(--muted-grey);
      font-size: 0.75rem;
      padding: 0.25rem 0.6rem;
      border-radius: 4px;
    }}

    /* Author Card */
    .author-card {{
      background: var(--charcoal);
      border: 1px solid var(--charcoal-border);
      border-radius: 12px;
      padding: 1.5rem;
      display: flex;
      gap: 1.25rem;
      align-items: center;
      margin-bottom: 2rem;
    }}
    .author-img {{
      width: 72px;
      height: 72px;
      border-radius: 50%;
      border: 2px solid var(--neon-lime);
      object-fit: cover;
      flex-shrink: 0;
    }}
    .author-info h4 {{
      font-size: 1rem;
      font-weight: 800;
      color: var(--off-white);
    }}
    .author-role {{ font-size: 0.8125rem; color: var(--neon-lime); margin-bottom: 0.25rem; }}
    .author-bio {{ font-size: 0.875rem; color: var(--muted-grey); line-height: 1.5; }}

    /* Sidebar */
    .sidebar-widget {{
      background: var(--charcoal);
      border: 1px solid var(--charcoal-border);
      border-radius: 12px;
      padding: 1.5rem;
      margin-bottom: 2rem;
    }}
    .widget-title {{
      font-size: 1rem;
      font-weight: 800;
      color: var(--off-white);
      margin-bottom: 1.25rem;
      border-bottom: 1px solid var(--charcoal-border);
      padding-bottom: 0.75rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .related-card {{
      margin-bottom: 1.25rem;
      display: flex;
      gap: 0.875rem;
      padding: 8px;
      border-radius: 8px;
      transition: background 0.2s, transform 0.2s;
    }}
    .related-card:hover {{
      background: rgba(255, 255, 255, 0.04);
      transform: translateX(2px);
    }}
    .related-thumb-link {{
      position: relative;
      width: 120px;
      height: 68px;
      flex-shrink: 0;
      border-radius: 6px;
      overflow: hidden;
      background: #000;
      display: block;
    }}
    .related-thumb-link img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
    }}
    .related-sport-pill {{
      position: absolute;
      top: 4px;
      left: 4px;
      background: rgba(0, 0, 0, 0.85);
      color: var(--neon-lime);
      font-size: 0.625rem;
      font-weight: 800;
      padding: 1px 4px;
      border-radius: 2px;
    }}
    .related-info {{ flex: 1; min-width: 0; }}
    .related-meta {{ font-size: 0.6875rem; color: var(--dark-grey); display: block; }}
    .related-title {{
      font-size: 0.8125rem;
      font-weight: 600;
      line-height: 1.35;
      margin-top: 0.2rem;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }}
    .related-title a {{ color: var(--off-white); }}
    .related-title a:hover {{ color: var(--neon-lime); text-decoration: none; }}
    .related-action-link {{
      font-size: 0.6875rem;
      font-weight: 700;
      color: var(--neon-lime);
      display: inline-block;
      margin-top: 4px;
    }}

    .catalog-cta-card {{
      background: linear-gradient(135deg, #151515 0%, #222222 100%);
      border: 1px solid var(--charcoal-border);
      border-radius: 12px;
      padding: 1.5rem;
      text-align: center;
    }}
    .catalog-cta-card h3 {{
      font-size: 1.125rem;
      font-weight: 800;
      margin-bottom: 0.5rem;
      color: var(--off-white);
    }}
    .catalog-cta-card p {{
      font-size: 0.875rem;
      color: var(--muted-grey);
      margin-bottom: 1.25rem;
    }}

    /* Footer */
    .site-footer {{
      border-top: 1px solid var(--charcoal-border);
      background: var(--pitch-black);
      padding: 2.5rem 1.5rem;
      color: var(--dark-grey);
      font-size: 0.875rem;
    }}
    .footer-container {{
      max-width: 1140px;
      margin: 0 auto;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 1rem;
    }}
    .footer-links {{ display: flex; gap: 1.5rem; list-style: none; }}
    .footer-links a {{ color: var(--muted-grey); }}
    .footer-links a:hover {{ color: var(--neon-lime); }}

    @media (max-width: 900px) {{
      .page-layout {{ grid-template-columns: 1fr; }}
      .article-h1 {{ font-size: 1.5rem; }}
      .main-nav {{ display: none; }}
      .mobile-toggle {{ display: block; }}
      .breadcrumb-current {{ max-width: 250px; }}
    }}
  </style>
</head>
<body>

  <!-- Google Tag Manager (noscript) -->
  <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-KFC9JGQJ" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
  <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-5N6XFRJ7" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>

  {render_navbar(active_page=sport)}

  <!-- Breadcrumbs -->
  <nav class="breadcrumb-bar" aria-label="Breadcrumb">
    <a href="/">Home</a>
    <span class="breadcrumb-sep">&gt;</span>
    <a href="{sport_hub_url}">{sport_name}</a>
    <span class="breadcrumb-sep">&gt;</span>
    <span class="breadcrumb-current">{video['title']}</span>
  </nav>

  <!-- Back Link -->
  <div class="back-link-bar">
    <a href="{sport_hub_url}" class="back-link">
      &larr; Back to {sport_name} Match Analysis Hub
    </a>
  </div>

  <!-- Main Content Layout -->
  <main class="page-layout">
    <article>
      <!-- Video Player Hero Box -->
      <section class="video-hero">
        <div class="video-aspect-frame">
          <iframe 
            src="https://www.youtube.com/embed/{vid}?rel=0" 
            title="{video['title']}" 
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
            allowfullscreen 
            loading="lazy"
          ></iframe>
        </div>

        <div class="video-meta-bar">
          <div class="meta-pills">
            <span class="sport-pill">{video['sport'].upper()}</span>
            <span class="playlist-pill">{video['playlist']}</span>
            <span class="views-pill">
              <svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>
              {video['views']}
            </span>
            <span style="font-size: 0.8125rem; color: var(--dark-grey);">· {video['read_time']}</span>
          </div>

          <h1 class="article-h1" lang="ml">{video['title']}</h1>

          <div class="cta-row">
            <a href="https://www.youtube.com/watch?v={vid}" target="_blank" rel="noopener noreferrer" class="btn btn-primary">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16" aria-hidden="true">
                <path d="M8.051 1.999h.089c.822.003 4.987.033 6.11.335a2.01 2.01 0 0 1 1.415 1.42c.101.38.172.883.22 1.402l.01.104.022.26.008.104c.065.914.073 1.77.074 1.957v.075c-.001.194-.01 1.108-.082 2.06l-.008.105-.009.104c-.05.572-.124 1.14-.235 1.558a2.007 2.007 0 0 1-1.415 1.42c-1.16.312-5.569.334-6.18.335h-.142c-.309 0-1.587-.006-2.927-.052l-.17-.006-.087-.004-.171-.007-.171-.007c-1.11-.049-2.167-.128-2.654-.26a2.007 2.007 0 0 1-1.415-1.419c-.111-.417-.185-.986-.235-1.558L.09 9.82l-.008-.104A31.4 31.4 0 0 1 0 7.68v-.123c.002-.215.01-.958.064-1.778l.007-.103.003-.052.008-.104.022-.26.01-.104c.048-.519.119-1.023.22-1.402a2.007 2.007 0 0 1 1.415-1.42c.487-.13 1.544-.21 2.654-.26l.17-.007.172-.006.086-.003.171-.007A99.788 99.788 0 0 1 7.858 2h.193zM6.4 5.209v4.818l4.157-2.408L6.4 5.209z"/>
              </svg>
              Watch on YouTube ↗
            </a>
            <a href="{sport_hub_url}" class="btn btn-outline">
              &larr; Back to {sport_name}
            </a>
          </div>
        </div>
      </section>

      <!-- Tactical Editorial Breakdown -->
      <section class="editorial-content">
        <h2>Tactical Breakdown &amp; Match Review | മലയാളം അവലോകനം</h2>
        <p lang="ml">{video['p1_ml']}</p>
        <p>{video['p2_en']}</p>

        <!-- Key Takeaways Box -->
        <div class="takeaways-box">
          <h3>Key Tactical Takeaways &amp; Discussion Points</h3>
          <ul>{takeaways_html}</ul>
        </div>

        <div class="tags-row">
          {tags_html}
        </div>

        <div style="margin-top: 1.5rem; padding-top: 1rem; border-top: 1px solid var(--charcoal-border);">
          <a href="{sport_hub_url}" class="btn btn-outline">
            &larr; Back to All {sport_name} Videos
          </a>
        </div>
      </section>

      <!-- Author Attribution Card -->
      <section class="author-card">
        <picture>
          <source srcset="/assets/images/haris-opt.webp" type="image/webp">
          <img src="/assets/images/haris-hero-portrait.png" alt="Haris Nenmara" class="author-img" width="72" height="72" loading="lazy">
        </picture>
        <div class="author-info">
          <h4>Analyzed by Haris Nenmara (ഹാരിസ് നെന്മാറ)</h4>
          <p class="author-role">Sports Journalist &amp; Tactical Analyst · Final Third</p>
          <p class="author-bio">Covering European football tactical systems, Kerala Blasters matchday dynamics in the ISL, and international cricket analysis in Malayalam.</p>
        </div>
      </section>
    </article>

    <!-- Sidebar Widget -->
    <aside>
      <div class="sidebar-widget">
        <h3 class="widget-title">
          <span>Related {video['sport'].capitalize()} Stories</span>
          <span style="font-size: 0.75rem; color: var(--neon-lime); font-weight: 700;">FINAL THIRD</span>
        </h3>
        {related_cards_html}
      </div>

      <div class="catalog-cta-card">
        <h3>300+ Video Analysis Archive</h3>
        <p>Explore our complete searchable catalog of football and cricket tactical breakdowns, player stories, and match debriefs.</p>
        <a href="/#videos" class="btn btn-primary" style="width: 100%; justify-content: center;">Browse Full Catalog →</a>
      </div>
    </aside>
  </main>

  <!-- Footer -->
  <footer class="site-footer">
    <div class="footer-container">
      <p>&copy; 2026 FINAL THIRD with Haris Nenmara. All rights reserved.</p>
      <ul class="footer-links">
        <li><a href="/">Home</a></li>
        <li><a href="/football/">Football Hub</a></li>
        <li><a href="/cricket/">Cricket Hub</a></li>
        <li><a href="/privacy.html">Privacy Policy</a></li>
        <li><a href="/#contact">Contact</a></li>
      </ul>
    </div>
  </footer>

  <script>
    // Mobile Drawer Toggle
    const mobileBtn = document.getElementById('mobileMenuToggle');
    const mobileDrawer = document.getElementById('mobileDrawer');
    if (mobileBtn && mobileDrawer) {{
      mobileBtn.addEventListener('click', function() {{
        const isOpen = mobileDrawer.classList.toggle('open');
        mobileBtn.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
      }});
    }}
  </script>

</body>
</html>
"""
    return html

# Render category hub listing page
def render_category_hub(sport):
    sport_name = "Football" if sport == "football" else "Cricket"
    other_sport = "cricket" if sport == "football" else "football"
    other_sport_name = "Cricket" if sport == "football" else "Football"
    sport_ml = "ഫുട്ബോൾ അവലോകനങ്ങൾ" if sport == "football" else "ക്രിക്കറ്റ് അവലോകനങ്ങൾ"
    meta_desc = (
        "Kerala's premier Malayalam football tactical analysis platform by Haris Nenmara. In-depth match debriefs, El Clasico, European leagues, and Kerala Blasters ISL breakdowns."
        if sport == "football" else
        "Malayalam cricket match analysis, tactical breakdowns, and player stories by Haris Nenmara. In-depth coverage of Sanju Samson, Jasprit Bumrah, Team India T20s, and World Cup moments."
    )

    vids = [v for v in VIDEOS if v["sport"] == sport]
    
    cards_html = ""
    for v in vids:
        page_url = f"/{sport}/{v['slug']}/"
        cards_html += f"""
        <article class="hub-card" onclick="window.location.href='{page_url}'" style="cursor: pointer;">
          <a href="{page_url}" class="hub-card-thumb-link" aria-label="{v['title']}">
            <img src="https://i.ytimg.com/vi/{v['id']}/hqdefault.jpg" alt="{v['title']}" width="480" height="270" loading="lazy" decoding="async">
            <span class="hub-card-badge">{v['playlist']}</span>
            <span class="hub-card-views">{v['views']}</span>
            <div class="hub-play-overlay" aria-hidden="true">
              <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="currentColor">
                <polygon points="5 3 19 12 5 21 5 3"></polygon>
              </svg>
            </div>
          </a>
          <div class="hub-card-body">
            <div class="hub-card-meta">
              <span class="hub-card-time">{v['published_iso'][:10]}</span>
              <span class="hub-card-dot">·</span>
              <span class="hub-card-read">{v['read_time']}</span>
            </div>
            <h2 class="hub-card-title"><a href="{page_url}">{v['title']}</a></h2>
            <p class="hub-card-snippet">{v['meta_desc']}</p>
            <div class="hub-card-footer">
              <a href="{page_url}" class="hub-card-btn">
                Read Tactical Breakdown &amp; Watch Video ↗
              </a>
            </div>
          </div>
        </article>"""

    hub_url = f"{DOMAIN}/{sport}/"

    html = f"""<!DOCTYPE html>
<html lang="en" xml:lang="ml" dir="ltr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{sport_name} Match Analysis &amp; Tactical Debriefs | Final Third with Haris Nenmara</title>
  <meta name="description" content="{meta_desc}">
  <meta name="author" content="Haris Nenmara (ഹാരിസ് നെന്മാറ)">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{hub_url}">

  <link rel="icon" type="image/png" sizes="32x32" href="/assets/images/favicon-32x32.png">

  <!-- Open Graph -->
  <meta property="og:site_name" content="Final Third with Haris Nenmara">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{hub_url}">
  <meta property="og:title" content="{sport_name} Tactical Analysis | Final Third">
  <meta property="og:description" content="{meta_desc}">
  <meta property="og:image" content="{DOMAIN}/assets/images/og-image.jpg">

  <!-- Twitter -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{sport_name} Tactical Analysis | Final Third">
  <meta name="twitter:description" content="{meta_desc}">
  <meta name="twitter:image" content="{DOMAIN}/assets/images/og-image.jpg">

  <!-- Tracking -->
  <script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
  new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
  j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
  'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
  }})(window,document,'script','dataLayer','GTM-KFC9JGQJ');</script>

  <script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
  new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
  j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
  'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
  }})(window,document,'script','dataLayer','GTM-5N6XFRJ7');</script>

  <script async src="https://www.googletagmanager.com/gtag/js?id=G-XR8PCQNHRE"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-XR8PCQNHRE');
  </script>

  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5399554232098923" crossorigin="anonymous"></script>

  <!-- Typography -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Anek+Malayalam:wght@400;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@graph": [
      {{
        "@type": "CollectionPage",
        "@id": "{hub_url}#collection",
        "url": "{hub_url}",
        "name": "{sport_name} Match Analysis | Final Third",
        "description": {json.dumps(meta_desc, ensure_ascii=False)},
        "isPartOf": {{
          "@id": "{DOMAIN}/#website"
        }}
      }},
      {{
        "@type": "BreadcrumbList",
        "@id": "{hub_url}#breadcrumb",
        "itemListElement": [
          {{
            "@type": "ListItem",
            "position": 1,
            "name": "Home",
            "item": "{DOMAIN}/"
          }},
          {{
            "@type": "ListItem",
            "position": 2,
            "name": "{sport_name} Analysis",
            "item": "{hub_url}"
          }}
        ]
      }}
    ]
  }}
  </script>

  <style>
    :root {{
      --neon-lime: #9EE20B;
      --neon-lime-hover: #b4f51e;
      --pitch-black: #080808;
      --charcoal: #151515;
      --charcoal-light: #202020;
      --charcoal-border: #2a2a2a;
      --off-white: #F5F5F0;
      --muted-grey: #a0a0a0;
      --dark-grey: #666666;
      --font-primary: 'Anek Malayalam', 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background: var(--pitch-black);
      color: var(--off-white);
      font-family: var(--font-primary);
      line-height: 1.6;
      -webkit-font-smoothing: antialiased;
    }}
    a {{ color: var(--neon-lime); text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}

    /* Header & Navigation */
    .site-header {{
      border-bottom: 1px solid var(--charcoal-border);
      background: rgba(8, 8, 8, 0.95);
      position: sticky;
      top: 0;
      z-index: 100;
      padding: 0.875rem 1.5rem;
      backdrop-filter: blur(10px);
    }}
    .nav-container {{ max-width: 1140px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; }}
    .brand-link {{ display: flex; align-items: center; gap: 0.75rem; color: var(--off-white); font-weight: 800; font-size: 1.125rem; }}
    .brand-logo {{ height: 36px; width: auto; display: block; }}
    .brand-name {{ font-weight: 800; color: var(--off-white); }}
    .main-nav {{ display: flex; align-items: center; }}
    .nav-list {{ display: flex; align-items: center; gap: 1.5rem; list-style: none; }}
    .nav-link {{ color: var(--muted-grey); font-weight: 600; font-size: 0.875rem; transition: color 0.2s; }}
    .nav-link:hover, .nav-link.active {{ color: var(--neon-lime); text-decoration: none; }}
    .nav-actions {{ display: flex; align-items: center; gap: 1rem; }}
    .btn-subscribe {{
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
      padding: 0.5rem 1rem;
      background: var(--neon-lime);
      color: #000;
      font-weight: 800;
      font-size: 0.8125rem;
      border-radius: 6px;
      text-decoration: none;
      transition: background-color 0.2s;
    }}
    .btn-subscribe:hover {{ background: var(--neon-lime-hover); text-decoration: none; }}
    .mobile-toggle {{
      display: none;
      background: none;
      border: none;
      color: var(--off-white);
      cursor: pointer;
    }}
    .mobile-drawer {{
      display: none;
      background: var(--charcoal);
      border-bottom: 1px solid var(--charcoal-border);
      padding: 1.5rem;
    }}
    .mobile-drawer.open {{ display: block; }}
    .drawer-list {{ list-style: none; display: flex; flex-direction: column; gap: 1rem; }}
    .drawer-link {{ color: var(--off-white); font-weight: 600; font-size: 1rem; text-decoration: none; }}
    .drawer-link.active {{ color: var(--neon-lime); }}

    /* Hub Hero */
    .hub-hero {{
      max-width: 1140px;
      margin: 1.5rem auto 0;
      padding: 2rem 1.5rem;
      border-bottom: 1px solid var(--charcoal-border);
    }}
    .hub-eyebrow {{
      color: var(--neon-lime);
      font-size: 0.8125rem;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      margin-bottom: 0.5rem;
    }}
    .hub-title {{
      font-size: 2.25rem;
      font-weight: 800;
      color: var(--off-white);
      line-height: 1.2;
      margin-bottom: 0.75rem;
    }}
    .hub-lead {{
      font-size: 1.0625rem;
      color: var(--muted-grey);
      max-width: 820px;
      line-height: 1.7;
      margin-bottom: 1.5rem;
    }}

    /* Sport Switcher Chips */
    .hub-switcher {{
      display: flex;
      align-items: center;
      gap: 10px;
      flex-wrap: wrap;
    }}
    .switch-chip {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 6px 14px;
      background: var(--charcoal);
      border: 1px solid var(--charcoal-border);
      border-radius: 999px;
      font-size: 0.8125rem;
      font-weight: 700;
      color: var(--off-white);
      text-decoration: none;
      transition: all 0.2s;
    }}
    .switch-chip:hover, .switch-chip.active {{
      background: rgba(158, 226, 11, 0.12);
      border-color: var(--neon-lime);
      color: var(--neon-lime);
      text-decoration: none;
    }}
    .switch-count {{
      background: rgba(255, 255, 255, 0.1);
      padding: 2px 6px;
      border-radius: 999px;
      font-size: 0.6875rem;
    }}
    .switch-chip.active .switch-count {{
      background: var(--neon-lime);
      color: #000;
    }}

    /* Hub Grid */
    .hub-grid {{
      max-width: 1140px;
      margin: 2rem auto 5rem;
      padding: 0 1.5rem;
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(330px, 1fr));
      gap: 1.75rem;
    }}

    .hub-card {{
      background: var(--charcoal);
      border: 1px solid var(--charcoal-border);
      border-radius: 12px;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      transition: transform 0.2s, border-color 0.2s, box-shadow 0.2s;
    }}
    .hub-card:hover {{
      transform: translateY(-4px);
      border-color: rgba(158, 226, 11, 0.5);
      box-shadow: 0 12px 28px rgba(0, 0, 0, 0.6);
    }}

    .hub-card-thumb-link {{
      position: relative;
      width: 100%;
      padding-top: 56.25%;
      display: block;
      background: #000;
      overflow: hidden;
    }}
    .hub-card-thumb-link img {{
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      object-fit: cover;
      transition: transform 0.3s ease;
    }}
    .hub-card:hover .hub-card-thumb-link img {{
      transform: scale(1.03);
    }}
    .hub-card-badge {{
      position: absolute;
      top: 8px;
      left: 8px;
      background: rgba(0, 0, 0, 0.85);
      color: var(--neon-lime);
      font-size: 0.6875rem;
      font-weight: 800;
      padding: 3px 6px;
      border-radius: 4px;
      z-index: 2;
    }}
    .hub-card-views {{
      position: absolute;
      bottom: 8px;
      right: 8px;
      background: rgba(0, 0, 0, 0.85);
      color: #fff;
      font-size: 0.6875rem;
      font-weight: 600;
      padding: 3px 6px;
      border-radius: 4px;
      z-index: 2;
    }}
    .hub-play-overlay {{
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      width: 48px;
      height: 48px;
      background: rgba(0, 0, 0, 0.75);
      border: 1px solid rgba(255, 255, 255, 0.2);
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      color: var(--neon-lime);
      opacity: 0.85;
      transition: all 0.2s;
      z-index: 2;
    }}
    .hub-card:hover .hub-play-overlay {{
      background: var(--neon-lime);
      color: #000;
      opacity: 1;
      transform: translate(-50%, -50%) scale(1.1);
    }}

    .hub-card-body {{ padding: 1.25rem; flex: 1; display: flex; flex-direction: column; }}
    .hub-card-meta {{
      font-size: 0.75rem;
      color: var(--dark-grey);
      margin-bottom: 0.4rem;
      display: flex;
      gap: 6px;
      align-items: center;
    }}
    .hub-card-dot {{ color: var(--dark-grey); }}
    .hub-card-read {{ color: var(--neon-lime); font-weight: 600; }}
    .hub-card-title {{
      font-size: 1.0625rem;
      font-weight: 700;
      line-height: 1.4;
      margin-bottom: 0.625rem;
    }}
    .hub-card-title a {{ color: var(--off-white); }}
    .hub-card-title a:hover {{ color: var(--neon-lime); text-decoration: none; }}
    .hub-card-snippet {{
      font-size: 0.8125rem;
      color: var(--muted-grey);
      line-height: 1.55;
      margin-bottom: 1.25rem;
      flex: 1;
    }}
    .hub-card-footer {{
      margin-top: auto;
      padding-top: 0.75rem;
      border-top: 1px solid var(--charcoal-border);
    }}
    .hub-card-btn {{
      font-size: 0.8125rem;
      font-weight: 700;
      color: var(--neon-lime);
      display: inline-flex;
      align-items: center;
      gap: 4px;
      transition: opacity 0.2s;
    }}
    .hub-card-btn:hover {{
      text-decoration: underline;
      opacity: 0.85;
    }}

    .site-footer {{
      border-top: 1px solid var(--charcoal-border);
      background: var(--pitch-black);
      padding: 2.5rem 1.5rem;
      color: var(--dark-grey);
      font-size: 0.875rem;
    }}
    .footer-container {{
      max-width: 1140px;
      margin: 0 auto;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 1rem;
    }}
    .footer-links {{ display: flex; gap: 1.5rem; list-style: none; }}
    .footer-links a {{ color: var(--muted-grey); }}
    .footer-links a:hover {{ color: var(--neon-lime); }}

    @media (max-width: 900px) {{
      .main-nav {{ display: none; }}
      .mobile-toggle {{ display: block; }}
      .hub-grid {{ grid-template-columns: 1fr; }}
      .hub-title {{ font-size: 1.75rem; }}
    }}
  </style>
</head>
<body>

  <!-- Google Tag Manager (noscript) -->
  <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-KFC9JGQJ" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
  <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-5N6XFRJ7" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>

  {render_navbar(active_page=sport)}

  <header class="hub-hero">
    <div class="hub-eyebrow">Category Listing · {sport_ml}</div>
    <h1 class="hub-title">{sport_name} Match Analysis &amp; Tactical Debriefs</h1>
    <p class="hub-lead">{meta_desc}</p>
    <div class="hub-switcher">
      <span style="font-size: 0.8125rem; color: var(--muted-grey); font-weight: 600;">Explore Categories:</span>
      <a href="/football/" class="switch-chip{' active' if sport == 'football' else ''}">
        ⚽ Football Analysis <span class="switch-count">14</span>
      </a>
      <a href="/cricket/" class="switch-chip{' active' if sport == 'cricket' else ''}">
        🏏 Cricket Analysis <span class="switch-count">6</span>
      </a>
      <a href="/#videos" class="switch-chip">
        📺 Full 300+ Archive <span class="switch-count">All</span>
      </a>
    </div>
  </header>

  <main class="hub-grid">
    {cards_html}
  </main>

  <footer class="site-footer">
    <div class="footer-container">
      <p>&copy; 2026 FINAL THIRD with Haris Nenmara. All rights reserved.</p>
      <ul class="footer-links">
        <li><a href="/">Home</a></li>
        <li><a href="/football/">Football Hub</a></li>
        <li><a href="/cricket/">Cricket Hub</a></li>
        <li><a href="/privacy.html">Privacy Policy</a></li>
        <li><a href="/#contact">Contact</a></li>
      </ul>
    </div>
  </footer>

  <script>
    // Mobile Drawer Toggle
    const mobileBtn = document.getElementById('mobileMenuToggle');
    const mobileDrawer = document.getElementById('mobileDrawer');
    if (mobileBtn && mobileDrawer) {{
      mobileBtn.addEventListener('click', function() {{
        const isOpen = mobileDrawer.classList.toggle('open');
        mobileBtn.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
      }});
    }}
  </script>

</body>
</html>
"""
    return html

def generate_all():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    
    print("=" * 60)
    print("Final Third — Generating Dedicated Video Pages & Hubs")
    print("=" * 60)

    # 1. Create Football & Cricket Hub Directories
    for sport in ["football", "cricket"]:
        sport_dir = os.path.join(base_dir, sport)
        os.makedirs(sport_dir, exist_ok=True)
        hub_html = render_category_hub(sport)
        with open(os.path.join(sport_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(hub_html)
        print(f"✓ Created /{sport}/ hub index.html")

    # 2. Create the 20 Dedicated Video Pages
    created_pages = []
    for v in VIDEOS:
        page_dir = os.path.join(base_dir, v["sport"], v["slug"])
        os.makedirs(page_dir, exist_ok=True)
        page_html = render_page(v)
        file_path = os.path.join(page_dir, "index.html")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(page_html)
        created_pages.append(f"/{v['sport']}/{v['slug']}/")
        print(f"  ⚡ [{v['sport'].upper()}] /{v['sport']}/{v['slug']}/")

    print(f"\n✓ Successfully created {len(created_pages)} dedicated video pages!")

    # 3. Generate Updated sitemap.xml with Video Extensions
    sitemap_path = os.path.join(base_dir, "sitemap.xml")
    sitemap_entries = [
        f"""  <url>
    <loc>{DOMAIN}/</loc>
    <lastmod>2026-10-30</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>""",
        f"""  <url>
    <loc>{DOMAIN}/football/</loc>
    <lastmod>2026-10-30</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.8</priority>
  </url>""",
        f"""  <url>
    <loc>{DOMAIN}/cricket/</loc>
    <lastmod>2026-10-30</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.8</priority>
  </url>""",
        f"""  <url>
    <loc>{DOMAIN}/privacy.html</loc>
    <lastmod>2026-10-30</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.5</priority>
  </url>"""
    ]

    for v in VIDEOS:
        vid_url = f"{DOMAIN}/{v['sport']}/{v['slug']}/"
        thumb_url = f"https://i.ytimg.com/vi/{v['id']}/maxresdefault.jpg"
        clean_title = v["title"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
        clean_desc = v["meta_desc"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
        
        sitemap_entries.append(f"""  <url>
    <loc>{vid_url}</loc>
    <lastmod>2026-10-30</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
    <video:video>
      <video:thumbnail_loc>{thumb_url}</video:thumbnail_loc>
      <video:title>{clean_title}</video:title>
      <video:description>{clean_desc}</video:description>
      <video:player_loc>https://www.youtube.com/embed/{v['id']}</video:player_loc>
      <video:publication_date>{v['published_iso']}</video:publication_date>
      <video:family_friendly>yes</video:family_friendly>
    </video:video>
  </url>""")

    full_sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:video="http://www.google.com/schemas/sitemap-video/1.1">
{chr(10).join(sitemap_entries)}
</urlset>
"""
    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write(full_sitemap)
    print(f"✓ Successfully generated sitemap.xml with {len(sitemap_entries)} entries (including 20 video extensions)!")

if __name__ == "__main__":
    generate_all()
