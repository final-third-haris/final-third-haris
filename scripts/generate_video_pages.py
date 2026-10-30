#!/usr/bin/env python3
"""
Final Third — Automated Generator for Dedicated Video SEO Pages & Category Hubs
Generates:
1. 20 dedicated, high-performance SEO video pages (14 Football, 6 Cricket)
2. Football category hub (/football/index.html)
3. Cricket category hub (/cricket/index.html)
4. Video sitemap (sitemap.xml) with complete Google Video metadata
5. Updated homepage video cards linking to dedicated pages
"""

import os
import json
import re
from datetime import datetime

DOMAIN = "https://www.finalthird-haris.com"

# 20 Selected High-Performing & Evergreen Videos (14 Football, 6 Cricket)
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
        "meta_desc": "In-depth tactical analysis of El Clasico between Real Madrid and Barcelona in Malayalam by Haris Nenmara. Breaking down formations, pressing triggers, and key match moments.",
        "published_iso": "2026-10-26T09:41:12+00:00",
        "views": "114K views",
        "read_time": "3 min read",
        "p1_ml": "എൽ ക്ലാസിക്കോ പോരാട്ടത്തിൽ റയൽ മാഡ്രിഡും ബാഴ്സലോണയും നേർക്കുനേർ വന്നപ്പോൾ കളിക്കളത്തിൽ പിറന്നത് ആധുനിക ഫുട്ബോളിന്റെ ഏറ്റവും മികച്ച തന്ത്രപരമായ വിരുന്നുകളിലൊന്നാണ്. ക്യാമ്പ് നൗവിൽ നടന്ന മത്സരത്തിൽ റയൽ മാഡ്രിഡിന്റെ ഹൈ-പ്രസ്സിങ് ഘടനയും കൗണ്ടർ-അറ്റാക്കിങ് വേഗവും ബാഴ്സയുടെ പ്രതിരോധത്തെ നിരന്തരം സമ്മർദ്ദത്തിലാക്കി. ഹോസെയുടെ തന്ത്രങ്ങളും കാർലോ ആഞ്ചലോട്ടിയുടെ ടീം ഷേപ്പും എങ്ങനെയെല്ലാമാണ് കളിയുടെ ഗതി മാറ്റിയതെന്ന് ഹാരിസ് നെന്മാറ ഈ വീഡിയോയിൽ കൃത്യമായി പരിശോധിക്കുന്നു.",
        "p2_en": "This tactical breakdown dissects the tactical setups of both European heavyweights. We examine how Real Madrid exploited transition spaces behind Barcelona's defensive high line, the positioning of wingers to isolate full-backs, and the midfield battle between both sides. Haris Nenmara breaks down why structural discipline and quick direct passes made the decisive difference in this fierce El Clasico showdown.",
        "takeaways": [
            "Exploitation of spaces behind Barcelona's aggressive high defensive block",
            "Midfield pressing triggers that disrupted build-up play from the back",
            "Rapid vertical transition play through wingers creating 1v1 overloads",
            "Key defensive adjustments made during second-half tactical phases"
        ],
        "tags": ["El Clasico", "Real Madrid", "Barcelona", "La Liga Tactics", "Haris Nenmara", "Football Analysis Malayalam"]
    },
    {
        "id": "RDpM-6xLCao",
        "slug": "barcelona-vs-real-madrid-hansi-flick-tactics",
        "sport": "football",
        "sport_title": "Football Analysis",
        "playlist": "Barcelona",
        "title": "ബാഴ്സയെ വീഴ്ത്താന്‍ കെല്‍പ്പുണ്ടോ റയലിന് ? Real madrid vs Barcelona | El clasico",
        "seo_title": "Can Real Madrid Beat Hansi Flick's Barcelona? El Clasico Tactical Preview",
        "meta_desc": "Hansi Flick's aggressive tactical approach at Barcelona scrutinized ahead of the Real Madrid El Clasico clash. Tactical debrief in Malayalam by Haris Nenmara.",
        "published_iso": "2026-10-24T11:17:04+00:00",
        "views": "55K views",
        "read_time": "3 min read",
        "p1_ml": "ഹാൻസി ഫ്ലിക്കിന്റെ കീഴിൽ പുതിയ ഊർജ്ജത്തോടെ കുതിക്കുന്ന ബാഴ്സലോണയെ തടഞ്ഞുനിർത്താൻ റയൽ മാഡ്രിഡിന് സാധിക്കുമോ? അതിവേഗത്തിലുള്ള ബോൾ റിക്കവറിയും കംപാക്റ്റ് ഹൈ-ലൈൻ ഡിഫൻസും അടിസ്ഥാനമാക്കിയുള്ള ബാഴ്സയുടെ ശൈലി ലാ ലിഗയിലെ ഏറ്റവും വലിയ ചോദ്യചിഹ്നമായി മാറിയിരിക്കുകയാണ്. എതിരാളികളുടെ പിഴവുകളെ വേഗത്തിൽ മുതലെടുക്കുന്ന ഫ്ലിക്കിന്റെ തന്ത്രങ്ങൾ എൽ ക്ലാസിക്കോയിൽ എത്രത്തോളം നിർണ്ണായകമാകുമെന്ന് ഈ വീഡിയോ വ്യക്തമാക്കുന്നു.",
        "p2_en": "An analytical exploration of Hansi Flick's tactical revolution at FC Barcelona. We evaluate their synchronized offside traps, fluid front three combinations, and spatial dominance in the final third. The analysis investigates whether Real Madrid's individual brilliance can bypass Barcelona's suffocating central pressing or if Flick's system will dictate terms.",
        "takeaways": [
            "Hansi Flick's synchronized offside trap execution and compact back line",
            "Central counter-pressing structures enabling instant possession regain",
            "Movement of attacking midfielders into half-spaces to break low blocks",
            "Potential vulnerabilities against elite speed in defensive transitions"
        ],
        "tags": ["Barcelona", "Hansi Flick", "El Clasico", "Real Madrid", "Tactical Preview", "La Liga"]
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
        "p1_ml": "യുവേഫ ചാമ്പ്യൻസ് ലീഗിൽ ബാഴ്സലോണയും പാരീസ് സെന്റ് ജെർമെയ്നും (PSG) തമ്മിൽ നടന്ന തീപാറുന്ന പോരാട്ടത്തിന്റെ സമഗ്രമായ അവലോകനം. കൗമാര വിസ്മയം ലാമിൻ യമാലിന്റെ അസാധാരണമായ വിങ്-പ്ലേയും ഡ്രിബ്ലിങ് വൈദഗ്ധ്യവും പിഎസ്ജിയുടെ ലെഫ്റ്റ്-ബാക്ക് പൊസിഷനെ എങ്ങിനെ തകിടം മറിച്ചുവെന്ന് ഹാരിസ് നെന്മാറ വിശദീകരിക്കുന്നു. യൂറോപ്യൻ വമ്പന്മാരുടെ കളിക്കളത്തിലെ തന്ത്രപരമായ ഏറ്റുമുട്ടൽ ഇതിൽ കാണാം.",
        "p2_en": "Focusing on the Champions League blockbuster between Barcelona and PSG, this video analyzes tactical dynamics in high-stakes knockout football. Discover how Lamine Yamal's isolation plays on the right flank stretched PSG's defensive shape, allowing interior runners to penetrate into dangerous attacking pockets.",
        "takeaways": [
            "Lamine Yamal's 1v1 dribbling statistics and box-entry creation",
            "PSG's tactical overload strategies in the attacking third",
            "Midfield distribution battles between Pedri and PSG's pivot",
            "Key defensive transitions under high European competition tempo"
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
        "meta_desc": "Can anyone stop this Barcelona team? Tactical investigation into Hansi Flick's tactical blueprint, Rodri comparisons, and Lamine Yamal's influence.",
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
        "p1_ml": "യൂറോപ്യൻ ഫുട്ബോളിൽ ആർബി ലെയ്പ്സിഗിനെതിരായ റയൽ മാഡ്രിഡിന്റെ പോരാട്ടം നൽകിയ തന്ത്രപരമായ മുന്നറിയിപ്പുകൾ പരിശോധിക്കുകയാണ് ഹാരിസ് നെന്മാറ. ജർമ്മൻ ടീമിന്റെ ഹൈ-ഇന്റൻസിറ്റി പ്രസ്സിങ്ങിന് മുന്നിൽ റയൽ നേരിട്ട വെല്ലുവിളികളും, പ്രതിരോധത്തിലെ വിടവുകൾ നികത്താൻ കാർലോ ആഞ്ചലോട്ടി നടത്തിയ പകരക്കാരെ ഇറക്കലും കളിയിലെ വഴിത്തിരിവുകളായി. ലാ ലിഗയിലെ മറ്റ് മത്സരങ്ങൾക്കും എൽ ക്ലാസിക്കോയ്ക്കും ഈ പോരാട്ടം നൽകുന്ന സന്ദേശങ്ങൾ എന്തൊക്കെയാണ്?",
        "p2_en": "Analyzing Real Madrid's resilience under tactical duress against RB Leipzig. This video studies how Leipzig's 4-2-2-2 system suffocated Madrid's central circulation and how individual tactical moments from Madrid's star players salvaged decisive momentum in crucial phases of the game.",
        "takeaways": [
            "Leipzig's narrow defensive shape forcing Madrid wide",
            "Defensive mid-block transitions and counter-attack containment",
            "Individual ball-carrying impact under sustained pressure",
            "Tactical lessons for Real Madrid heading into top-flight fixtures"
        ],
        "tags": ["Real Madrid", "RB Leipzig", "Champions League", "Tactical Breakdown", "Carlo Ancelotti", "Haris Nenmara"]
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
        "p1_ml": "എഎസ് റോമയ്ക്കെതിരായ റയൽ മാഡ്രിഡിന്റെ ഗംഭീര പ്രകടനം ഫുട്ബോൾ പ്രേമികൾക്ക് സമ്മാനിച്ചത് നിരവധി തന്ത്രപരമായ പാഠങ്ങളാണ്. ആക്രമണ നിരയിലെ ഫ്ലൂയിഡിറ്റിയും മധ്യനിരയിലെ നിയന്ത്രണവും എതിരാളികളെ പ്രതിരോധത്തിലാക്കിയെങ്കിലും, പ്രതിരോധത്തിൽ ഇനിയും പരിഹരിക്കപ്പെടേണ്ട ചില ദൗർബല്യങ്ങൾ ഈ മത്സരം തുറന്നുകാട്ടുന്നു. ഹാരിസ് നെന്മാറയുടെ സവിശേഷമായ വിശകലനം ഇവിടെ കാണാം.",
        "p2_en": "A detailed technical review of Real Madrid's tactical encounter with Italian side AS Roma. The analysis reviews positional interchangeability in Madrid's front three, box-crashing runs from central midfielders, and areas of defensive concentration that require calibration ahead of tournament knockouts.",
        "takeaways": [
            "Positional rotations between wingers and false nine attackers",
            "Box entries via progressive vertical passes",
            "Defensive transition vulnerabilities against pace on the counter",
            "Midfield tempo orchestration in controlling the rhythm of play"
        ],
        "tags": ["Real Madrid", "Roma", "Match Analysis", "European Football", "Tactical Debrief", "Final Third"]
    },
    {
        "id": "RtpY-aKasEg",
        "slug": "barcelona-vs-galatasaray-lamine-yamal-analysis",
        "sport": "football",
        "sport_title": "Football Analysis",
        "playlist": "Barcelona",
        "title": "ആളറിഞ്ഞു കളിക്കടാ ! barcelona vs galatasaray | lamine yamal | Haris Nenmara",
        "seo_title": "Barcelona vs Galatasaray Match Review | Lamine Yamal Performance Analysis",
        "meta_desc": "Barcelona vs Galatasaray tactical match review in Malayalam. How Lamine Yamal and Barcelona broke down aggressive defensive setups with tactical flair.",
        "published_iso": "2026-10-19T14:00:00+00:00",
        "views": "72K views",
        "read_time": "3 min read",
        "p1_ml": "തുർക്കിഷ് കരുത്തരായ ഗലാത്സരെയ്ക്കെതിരെ ബാഴ്സലോണ നടത്തിയ പോരാട്ടത്തിൽ കളിയുടെ നിയന്ത്രണം പിടിച്ചെടുത്തത് തന്ത്രപരമായ പക്വതയാണ്. എതിർ ടീമിന്റെ കടുത്ത വെല്ലുവിളികളെയും ശാരീരികമായ അഗ്രഷനെയും അതിജീവിച്ച് ബാഴ്സലോണ തങ്ങളുടെ സ്വാഭാവിക പാസിങ് ഗെയിം എങ്ങനെ പുറത്തെടുത്തുവെന്ന് ഈ വീഡിയോ വിശദീകരിക്കുന്നു. ലാമിൻ യമാലിന്റെ ക്ലാസ് പ്രകടനവും മത്സരത്തിൽ നിർണ്ണായകമായി.",
        "p2_en": "Reviewing Barcelona's tactical composure against Galatasaray's combative defensive block. Haris Nenmara analyzes how patience in build-up, precision diagonal switches, and individual flair dismantled the opponent's aggressive defensive strategy.",
        "takeaways": [
            "Overcoming aggressive man-marking through quick one-touch passing",
            "Diagonal long-ball switches to exploit the under-defended flank",
            "Lamine Yamal's decisive playmaking in the final third",
            "Patience and positional discipline against low defensive blocks"
        ],
        "tags": ["Barcelona", "Galatasaray", "Lamine Yamal", "European Football", "Match Review", "Haris Nenmara"]
    },
    {
        "id": "l1q1MQZSe_0",
        "slug": "kerala-blasters-sanan-momo-fitness-tactics",
        "sport": "football",
        "sport_title": "Football Analysis",
        "playlist": "Kerala Blasters & Indian Football",
        "title": "'സനാന് ഫിറ്റ്നസില്ല... മോമോയുടെ  മെന്‍റാലിറ്റി'; ആഷ്‍ലിയുടെ തുറന്ന് പറച്ചിലുകള്‍ | Kerala blasters",
        "seo_title": "Kerala Blasters Player Fitness & Mental Approach Analysis | ISL Tactical Review",
        "meta_desc": "Kerala Blasters player fitness, tactical discipline, and mentality analyzed by Haris Nenmara. In-depth review of Sanan, Momo, and ISL campaign requirements.",
        "published_iso": "2026-10-18T10:00:00+00:00",
        "views": "55K views",
        "read_time": "3 min read",
        "p1_ml": "കേരള ബ്ലാസ്റ്റേഴ്സിന്റെ ഈ സീസണിലെ പ്രകടനങ്ങളെയും ടീം മാനേജ്മെന്റിന്റെ നിലപാടുകളെയും വിലയിരുത്തുന്ന സമഗ്രമായ ചർച്ച. മുഹമ്മദ് സനാന്റെ ഫിറ്റ്നസ് ലെവലുകളെക്കുറിച്ചും മോമോ യാൻസന്റെ ഫൈറ്റിങ് മെന്റാലിറ്റിയെക്കുറിച്ചും പുറത്തുവന്ന വെളിപ്പെടുത്തലുകൾ ബ്ലാസ്റ്റേഴ്സ് ക്യാമ്പിലെ യാഥാർത്ഥ്യങ്ങളിലേക്ക് വിരൽചൂണ്ടുന്നു. ഐഎസ്എല്ലിൽ മുന്നേറാൻ സാങ്കേതിക തികവിനൊപ്പം ശാരീരിക ക്ഷമത എത്രത്തോളം പ്രധാനമാണെന്ന് ഹാരിസ് നെന്മാറ പങ്കുവെക്കുന്നു.",
        "p2_en": "A critical examination of player development and squad depth at Kerala Blasters FC. This video analyzes the technical potential of Indian youngsters like Sanan alongside the physical and psychological demands of the Indian Super League (ISL), highlighting why tactical consistency demands elite fitness standards.",
        "takeaways": [
            "The physical intensity benchmarks required in the modern ISL",
            "Tactical balance between flair players and high-work-rate runners",
            "Squad rotation challenges facing Kerala Blasters coaching staff",
            "Mentality and resilience needed in crunch matchday scenarios"
        ],
        "tags": ["Kerala Blasters", "ISL", "Indian Football", "Sanan", "Momo Yansane", "Haris Nenmara"]
    },
    {
        "id": "ySpbZe77Jgs",
        "slug": "kerala-blasters-fallou-ndiaye-defensive-wall",
        "sport": "football",
        "sport_title": "Football Analysis",
        "playlist": "Kerala Blasters & Indian Football",
        "title": "ഫാലു ബാക്ക് ; ബ്ലാസ്റ്റേഴ്സ് ബാക്ക് ലൈൻ സുശക്തം | Fallou ndiaye| Kerala Blasters",
        "seo_title": "Fallou Ndiaye & Kerala Blasters Defensive Line Tactical Analysis | ISL",
        "meta_desc": "How Fallou Ndiaye reinforces the Kerala Blasters defense. Tactical analysis of defensive shape, aerial duels, and clean sheets in the ISL by Haris Nenmara.",
        "published_iso": "2026-10-15T12:00:00+00:00",
        "views": "35K views",
        "read_time": "3 min read",
        "p1_ml": "കേരള ബ്ലാസ്റ്റേഴ്സിന്റെ പ്രതിരോധ കോട്ടയ്ക്ക് കാവലാളായി ഫാലു എൻദിയായെ തിരികെയെത്തുമ്പോൾ ടീമിന്റെ ഗെയിം പ്ലാനിൽ വരുന്ന മാറ്റങ്ങൾ എന്തൊക്കെയാണ്? ഗ്രൗണ്ടിലെ എയറിയൽ ഡോമിനൻസും ലീഡർഷിപ്പ് ക്വാളിറ്റിയും ബ്ലാസ്റ്റേഴ്സിന്റെ ബോക്സ് പ്രതിരോധത്തെ എത്രത്തോളം ശക്തമാക്കുന്നു എന്ന് ഈ വീഡിയോ വിശകലനം ചെയ്യുന്നു. പ്രതിരോധ പിഴവുകൾ കുറച്ച് ക്ലീൻ ഷീറ്റുകൾ നിലനിർത്താൻ ഫാലുവിന്റെ തിരിച്ചുവരവ് നൽകുന്ന മുൻതൂക്കം ഇതിൽ ചർച്ചയാകുന്നു.",
        "p2_en": "Analyzing the tactical impact of center-back Fallou Ndiaye on Kerala Blasters' defensive solidity. We break down defensive line height, aerial duel win rates, box defending, and how a confident ball-playing defender stabilizes build-up under pressure from opposition forwards.",
        "takeaways": [
            "Commanding aerial presence in defending set-pieces and crosses",
            "Communication and organization of the defensive back four",
            "Calm progressive passing out of the defensive defensive third",
            "Impact on goalkeeper confidence and reducing conceded shots on target"
        ],
        "tags": ["Kerala Blasters", "Fallou Ndiaye", "ISL Defense", "Indian Football", "Tactical Review"]
    },
    {
        "id": "cOYjZ39qHAU",
        "slug": "kerala-blasters-momo-yanson-attack-bolton-defense",
        "sport": "football",
        "sport_title": "Football Analysis",
        "playlist": "Kerala Blasters & Indian Football",
        "title": "അറ്റാക്കിൽ യാൻസൺ ; കോട്ട കാക്കാൻ ബോൾട്ടൻ | Kerala Blasters | Momo yansane | James Bolton",
        "seo_title": "Kerala Blasters Tactical Balance: Yansane Attack & Bolton Defense | ISL",
        "meta_desc": "Kerala Blasters tactical balance: Momo Yansane spearheading the attack and James Bolton commanding the defense. Detailed ISL tactical debrief.",
        "published_iso": "2026-10-14T11:00:00+00:00",
        "views": "60K views",
        "read_time": "3 min read",
        "p1_ml": "മുന്നേറ്റ നിരയിൽ മോമോ യാൻസന്റെ ഗോളടി മികവും പ്രതിരോധത്തിൽ ജെയിംസ് ബോൾട്ടന്റെ പരിചയസമ്പത്തും ചേരുമ്പോൾ കേരള ബ്ലാസ്റ്റേഴ്സിന് ലഭിക്കുന്ന തന്ത്രപരമായ സന്തുലിതാവസ്ഥ പരിശോധിക്കുന്ന വീഡിയോ. കൗണ്ടർ അറ്റാക്കുകളിൽ യാൻസന്റെ സ്പീഡും ബോക്സിലെ ഫിനിഷിങ്ങും ടീമിന് എത്രത്തോളം കരുത്തുപകരുന്നു? മറുവശത്ത് ബോൾട്ടന്റെ സാന്നിധ്യം പ്രതിരോധത്തെ എങ്ങനെ സുരക്ഷിതമാക്കുന്നു? ഹാരിസ് നെന്മാറ വിശദീകരിക്കുന്നു.",
        "p2_en": "Evaluating the tactical spine of Kerala Blasters FC. This video breaks down the dual dynamic of Momo Yansane's physical focal-point hold-up play in attack and James Bolton's defensive experience in organizing the offside line and managing spatial threats.",
        "takeaways": [
            "Hold-up and link-up play from the central target striker",
            "Defensive anticipation and blocking dangerous interior passing lanes",
            "Tactical balance between aggressive attack and defensive rest-defense",
            "Key partnerships driving Kerala Blasters' competitive ambitions"
        ],
        "tags": ["Kerala Blasters", "Momo Yansane", "James Bolton", "ISL", "Indian Super League", "Tactical Analysis"]
    },
    {
        "id": "Ustsj3NHM4Y",
        "slug": "kerala-blasters-midfield-nebojsa-kosovic-tactics",
        "sport": "football",
        "sport_title": "Football Analysis",
        "playlist": "Kerala Blasters & Indian Football",
        "title": "ബ്ലാസ്റ്റേഴ്സ് മധ്യനിര ഇനി കൊസോവിച്ച് ഭരിക്കും | Kerala Blasters | Nebojša Kosović",
        "seo_title": "Nebojsa Kosovic Midfield Masterclass & Kerala Blasters Tactics | ISL",
        "meta_desc": "How Nebojsa Kosovic controls the Kerala Blasters midfield tempo. Passing vision, spatial control, and tactical debrief in Malayalam by Haris Nenmara.",
        "published_iso": "2026-10-13T10:00:00+00:00",
        "views": "87K views",
        "read_time": "3 min read",
        "p1_ml": "കേരള ബ്ലാസ്റ്റേഴ്സിന്റെ മധ്യനിരയുടെ താളവും വേഗതയും നിയന്ത്രിക്കുന്നതിൽ നെബോയ്ഷ കൊസോവിച്ച് എന്ന മിഡ്ഫീൽഡ് ജനറലിന്റെ പ്രാധാന്യം വ്യക്തമാക്കുന്ന അവലോകനം. ബോൾ ഡിസ്ട്രിബ്യൂഷനിലെ കൃത്യത, പ്രതിരോധത്തിൽ നിന്നും പന്ത് സ്വീകരിച്ച് മുന്നേറ്റ നിരയിലേക്ക് പകർന്നുനൽകാനുള്ള കഴിവ്, മത്സരത്തിന്റെ ടെമ്പോ നിയന്ത്രിക്കൽ എന്നിവയിലൂടെ കൊസോവിച്ച് ബ്ലാസ്റ്റേഴ്സിന് നൽകുന്ന അധിക ആനുകൂല്യങ്ങൾ എന്തൊക്കെയാണെന്ന് പരിശോധിക്കാം.",
        "p2_en": "Deep technical analysis of Nebojsa Kosovic's midfield playmaking profile for Kerala Blasters. We assess pass completion rates under press, progressive line-breaking deliveries, positional awareness, and his ability to dictate game tempo across demanding ISL matches.",
        "takeaways": [
            "Controlling the tempo through short-long passing variance",
            "Shielding the central center-backs against direct attacks",
            "Creating numerical overloads in the central third of the pitch",
            "Set-piece delivery accuracy and tactical awareness in transition"
        ],
        "tags": ["Kerala Blasters", "Nebojsa Kosovic", "ISL Midfield", "Football Analysis", "Indian Football"]
    },
    {
        "id": "ZuU9k-lVTzE",
        "slug": "kerala-blasters-aston-villa-green-new-signings",
        "sport": "football",
        "sport_title": "Football Analysis",
        "playlist": "Kerala Blasters & Indian Football",
        "title": "ആസ്റ്റൺ വില്ലയിൽ നിന്ന് കളി പഠിച്ച ഗ്രീൻ;കൊമ്പന്മാരുടെ പുതിയ സൈനിംഗുകൾ| Kerala Blasters New signings",
        "seo_title": "Aston Villa Pedigree: Kerala Blasters New Signings & Tactical Role",
        "meta_desc": "Aston Villa academy background meets Kerala Blasters FC. Technical evaluation of the new foreign signings and their tactical fit in the ISL by Haris Nenmara.",
        "published_iso": "2026-10-12T14:00:00+00:00",
        "views": "111K views",
        "read_time": "3 min read",
        "p1_ml": "ഇംഗ്ലീഷ് പ്രീമിയർ ലീഗ് ക്ലബ്ബ് ആസ്റ്റൺ വില്ലയുടെ അക്കാദമിയിൽ നിന്നും കളിയഭ്യസിച്ച താരങ്ങളുടെ വരവ് കേരള ബ്ലാസ്റ്റേഴ്സിന്റെ നിലവാരത്തെ എങ്ങനെയെല്ലാമാണ് ഉയർത്തുന്നത്? പുതിയ സീസണിലേക്കായി ബ്ലാസ്റ്റേഴ്സ് മാനേജ്മെന്റ് നടത്തിയ മികച്ച സൈനിങ്ങുകളുടെ സാങ്കേതിക മേന്മകളും, അവർ ടീമിന്റെ സിസ്റ്റത്തിൽ എങ്ങനെ ഫിറ്റാകും എന്നതും വിശദമായി പരിശോധിക്കുന്ന വീഡിയോ.",
        "p2_en": "Examining the footballing pedigree and tactical attributes of Kerala Blasters' new arrivals with Premier League academy backgrounds. We investigate positional flexibility, technical fundamentals, and how European football training translates to the physical environment of the Indian Super League.",
        "takeaways": [
            "Technical foundations honed in elite English youth academies",
            "High footballing IQ and quick decision-making under tight pressure",
            "Tactical flexibility across multiple roles in attacking and midfield setups",
            "Elevating team passing accuracy and combination speed in the final third"
        ],
        "tags": ["Kerala Blasters", "Aston Villa", "New Signings", "ISL Transfers", "Indian Football", "Haris Nenmara"]
    },
    {
        "id": "rNiXi4pW9nM",
        "slug": "lionel-messi-football-legacy-tactics",
        "sport": "football",
        "sport_title": "Football Analysis",
        "playlist": "World Cup & Football Legends",
        "title": "ഇങ്ങനെ ഒരിതിഹാസം ഇനി പിറക്കുമോ ? Lionel Messi | Haris Nenmara",
        "seo_title": "Lionel Messi Tactical Genius & Enduring Legacy | Final Third Football Special",
        "meta_desc": "Lionel Messi's tactical genius, spatial awareness, and career legacy analyzed in Malayalam by Haris Nenmara. The greatest football breakdown.",
        "published_iso": "2026-10-10T12:00:00+00:00",
        "views": "65K views",
        "read_time": "3 min read",
        "p1_ml": "ഫുട്ബോൾ ചരിത്രത്തിലെ ഏറ്റവും മഹാനായ കളിക്കാരനായ ലയണൽ മെസ്സിയുടെ തന്ത്രപരമായ പ്രതിഭയെയും അവിസ്മരണീയമായ കരിയറിനെയും അടയാളപ്പെടുത്തുന്ന സ്പെഷ്യൽ വീഡിയോ. സാധാരണ കളിക്കാർ കാണാത്ത സ്പേസുകൾ കണ്ടെത്താനുള്ള മെസ്സിയുടെ വിഷൻ, ചെറിയ ഇടങ്ങളിലെ ഡ്രിബ്ലിങ് നിയന്ത്രണം, ഗോളിന് മുന്നിലെ കാംനസ് എന്നിവയെല്ലാം ഫുട്ബോളിന്റെ സൌന്ദര്യശാസ്ത്രമായി മാറിയത് എങ്ങനെയെന്ന് ഹാരിസ് നെന്മാറ വിശദീകരിക്കുന്നു.",
        "p2_en": "A tribute and tactical dissection of Lionel Messi's career-defining qualities. From false nine movement under Guardiola to deep-lying playmaker roles in international triumphs, we break down Messi's walking telemetry, scan rates, and unmatched playmaking output in world football history.",
        "takeaways": [
            "Head scan frequency and pitch spatial mapping before receiving the ball",
            "The mechanics of decelerating and shifting momentum in 1v1 dribbles",
            "Transition from inverted winger to generational false nine and deep creator",
            "Clutch performance metrics in World Cup and European tournament finals"
        ],
        "tags": ["Lionel Messi", "Football Legend", "Tactical Genius", "World Cup", "Argentina", "Haris Nenmara"]
    },
    {
        "id": "mVR_mRYU2YE",
        "slug": "cristiano-ronaldo-cr7-tactical-philosophy",
        "sport": "football",
        "sport_title": "Football Analysis",
        "playlist": "World Cup & Football Legends",
        "title": "കോച്ചോ  റോണോയോ; ആരാണ് ശരി? | Cristiano Ronaldo | Ronaldo Walkout | CR7",
        "seo_title": "Cristiano Ronaldo Tactical Role & Manager Dynamics | CR7 Analysis",
        "meta_desc": "Cristiano Ronaldo's tactical demands, box positioning, and team dynamics analyzed in Malayalam by Haris Nenmara. A neutral football debrief.",
        "published_iso": "2026-10-09T14:00:00+00:00",
        "views": "108K views",
        "read_time": "3 min read",
        "p1_ml": "ക്രിസ്റ്റ്യാനോ റൊണാൾഡോ എന്ന ഇതിഹാസ താരത്തിന്റെ കളിക്കളത്തിലെ റോളും മാനേജർമാരുടെ തന്ത്രപരമായ സമീപനങ്ങളും തമ്മിലുള്ള സംഘർഷങ്ങൾ പരിശോധിക്കുന്ന വീഡിയോ. പ്രായത്തെ വെല്ലുന്ന ഫിനിഷിങ് മികവും അത്‌ലറ്റിസിസവും നിലനിർത്തുമ്പോഴും ആധുനിക ഫുട്ബോളിന്റെ ഹൈ-പ്രസ്സിങ് ആവശ്യകതകളുമായി ഒരു സൂപ്പർ താരം എങ്ങനെ പൊരുത്തപ്പെടുന്നു? ഹാരിസ് നെന്മാറയുടെ നിഷ്പക്ഷവും ആഴത്തിലുള്ളതുമായ വിശകലനം.",
        "p2_en": "Analyzing the tactical friction between modern collective pressing systems and the lethal box-finishing profile of Cristiano Ronaldo. We evaluate box-movement geometry, aerial heading physics, and how elite managers structure team balance around an undisputed goal-scoring phenomenon.",
        "takeaways": [
            "Box movement timing creating separation from man-markers",
            "Aerial duel biomechanics and leaping leverage on set pieces",
            "Balancing pressing work-rates with penalty-box poaching efficiency",
            "The evolving tactical requirements of modern legendary center-forwards"
        ],
        "tags": ["Cristiano Ronaldo", "CR7", "Football Analysis", "Real Madrid", "Portugal", "Haris Nenmara"]
    },

    # ========================== CRICKET (6) ==========================
    {
        "id": "qDn--g-xzQY",
        "slug": "abhishek-sharma-vaibhav-suryavanshi-ind-vs-nz",
        "sport": "cricket",
        "sport_title": "Cricket Analysis",
        "playlist": "Cricket Stories & Analysis",
        "title": "ബ്രൂട്ടൽ; അഭിഷേകും വൈഭവവും ചേർന്ന് കിവികളെ കുഴിച്ച് മൂടി | Abhishek Sharma | Vaibhav Suryavanshi",
        "seo_title": "Abhishek Sharma & Vaibhav Brutal Batting vs New Zealand | Cricket Analysis",
        "meta_desc": "Brutal power-hitting: Abhishek Sharma and Vaibhav Suryavanshi dismantle New Zealand bowling. In-depth cricket analysis in Malayalam by Haris Nenmara.",
        "published_iso": "2026-10-25T14:00:00+00:00",
        "views": "281K views",
        "read_time": "3 min read",
        "p1_ml": "ന്യൂസിലൻഡിനെതിരായ ടി20 പോരാട്ടത്തിൽ അഭിഷേക് ശർമ്മയും വൈഭവ് സൂര്യവംശിയും ചേർന്ന് പുറത്തെടുത്തത് ആധുനിക ടി20 ക്രിക്കറ്റിന്റെ വിനാശകരമായ ബാറ്റിങ് വിരുന്നാണ്. പവർപ്ലേ ഓവറുകളിൽ ന്യൂസിലൻഡ് ബൗളർമാരുടെ ലൈനും ലെങ്തും തകർത്തുകൊണ്ട് കളിച്ച ഷോട്ടുകളുടെ കൃത്യതയും സാങ്കേതികതയും ഹാരിസ് നെന്മാറ പരിശോധിക്കുന്നു. ഭയമില്ലാത്ത ഈ ക്രിക്കറ്റ് ശൈലി ഇന്ത്യൻ ടീമിന്റെ ടി20 ഭാവിക്ക് നൽകുന്ന പുത്തൻ ദിശാബോധം എന്തൊക്കെയാണ്?",
        "p2_en": "A comprehensive cricket tactical breakdown of modern aggressive batting against quality pace and spin. This video analyzes bat-speed, base stability against short deliveries, boundary percentage through the powerplay, and how fearless top-order intent reshapes T20 match outcomes.",
        "takeaways": [
            "Maximizing powerplay run-rates through intent and boundary targeting",
            "Weight transfer and clean bat swing against international pace bowling",
            "Disrupting bowler field placements with innovative 360-degree shot making",
            "The evolving fearless mindset defining India's new generation of T20 batters"
        ],
        "tags": ["Abhishek Sharma", "Vaibhav Suryavanshi", "India vs New Zealand", "T20 Cricket", "Cricket Analysis Malayalam", "Haris Nenmara"]
    },
    {
        "id": "Xq1PtXOrVRc",
        "slug": "sanju-samson-redemption-story-india-vs-nz",
        "sport": "cricket",
        "sport_title": "Cricket Analysis",
        "playlist": "Cricket Stories & Analysis",
        "title": "സഞ്ജുവിൻ്റെ പ്രതികാര കഥ തുടരുന്നു ! Sanju Samson",
        "seo_title": "Sanju Samson Redemption Story & Match-Winning Knocks | Cricket Analysis",
        "meta_desc": "Sanju Samson's tactical resurgence, stroke play, and match-winning performances for Team India. Complete cricket analysis by Haris Nenmara.",
        "published_iso": "2026-10-22T14:50:51+00:00",
        "views": "175K views",
        "read_time": "3 min read",
        "p1_ml": "മലയാളികളുടെ പ്രിയ താരം സഞ്ജു സാംസണിന്റെ കരിയറിലെ ഏറ്റവും നിർണ്ണായകമായ ഘട്ടങ്ങളെയും അദ്ദേഹത്തിന്റെ തിരിച്ചുവരവുകളെയും ആഴത്തിൽ വിശകലനം ചെയ്യുന്ന വീഡിയോ. തുടർച്ചയായ അവഗണനകൾക്കും സമ്മർദ്ദങ്ങൾക്കും നടുവിൽ ക്രീസിലെത്തുമ്പോൾ സഞ്ജു പുറത്തെടുക്കുന്ന പക്വതയും, ഷോട്ട് സെലക്ഷനിലെ പുരോഗതിയും അദ്ദേഹത്തെ വിശ്വസ്തനായ മാച്ച് വിന്നറാക്കി മാറ്റുന്നത് എങ്ങനെയെന്ന് ഹാരിസ് നെന്മാറ വിശദീകരിക്കുന്നു.",
        "p2_en": "A technical and psychological assessment of Sanju Samson's evolution as an international top-order batter. We break down his balance at the crease, improved shot selection against hard lengths, temperament during middle-overs consolidation, and boundary acceleration against spin.",
        "takeaways": [
            "Balance and head position enabling effortless lofted shots over extra cover",
            "Adaptation against variations in pace and back-of-length bowling",
            "Patience in strike rotation leading to calculated boundary expansion",
            "Mental toughness and consistency under relentless selection scrutiny"
        ],
        "tags": ["Sanju Samson", "Team India", "Cricket Analysis", "T20 Cricket", "Sanju Samson Batting", "Haris Nenmara"]
    },
    {
        "id": "I-40yws8G-E",
        "slug": "sanju-samson-ind-vs-nz-match-answers",
        "sport": "cricket",
        "sport_title": "Cricket Analysis",
        "playlist": "Cricket Stories & Analysis",
        "title": "സഞ്ജുവിൻ്റെ മറുപടികൾ കൊള്ളുന്നത് ആർക്കാണ് ? Sanju Samson | Ind Vs Nz",
        "seo_title": "Sanju Samson Silences Critics: Ind vs NZ Match Breakdown | Final Third",
        "meta_desc": "Sanju Samson silences critics with decisive performance in India vs New Zealand. Cricket match review and tactical takeaways by Haris Nenmara.",
        "published_iso": "2026-10-23T13:57:49+00:00",
        "views": "85K views",
        "read_time": "3 min read",
        "p1_ml": "വിമർശകർക്ക് കളിക്കളത്തിലെ ബാറ്റുകൊണ്ട് തന്നെ മറുപടി നൽകി സഞ്ജു സാംസൺ വീണ്ടും തിളങ്ങിയ ഇന്ത്യ-ന്യൂസിലൻഡ് മത്സരത്തിന്റെ സമഗ്രമായ റിവ്യൂ. ബാറ്റിങ് ഓർഡറിലെ അനിശ്ചിതത്വങ്ങൾക്കിടയിലും ലഭിച്ച അവസരത്തെ പരമാവധി പ്രയോജനപ്പെടുത്തി ടീമിനെ വിജയത്തിലേക്ക് നയിക്കാൻ സഞ്ജുവിന് സാധിച്ചത് എങ്ങനെയാണ്? ഈ ഇന്നിങ്സ് ഇന്ത്യൻ ടീം മാനേജ്മെന്റിന് നൽകുന്ന ശക്തമായ സന്ദേശങ്ങൾ എന്തൊക്കെയാണ്?",
        "p2_en": "Breaking down Sanju Samson's match-defining performance against the Black Caps. We study his pacing through different phases of the innings, running between wickets, strike-rate management in challenging pitch conditions, and ability to hit clean boundaries without taking unwarranted risks.",
        "takeaways": [
            "Pacing the innings according to pitch behavior and match requirements",
            "Dominating spinners through footwork and precision placement",
            "Calm leadership on the field and positive body language",
            "Securing his rightful spot in India's limited-overs tactical blueprint"
        ],
        "tags": ["Sanju Samson", "Ind vs Nz", "Cricket Review", "Team India", "T20 Match", "Final Third Cricket"]
    },
    {
        "id": "F1X3eE_CBKU",
        "slug": "tilak-varma-naman-dhir-comeback-analysis",
        "sport": "cricket",
        "sport_title": "Cricket Analysis",
        "playlist": "Cricket Stories & Analysis",
        "title": "ഇതൊക്കെയാണ് കം ബാക്ക് ! നമൻ ധീർ പ്രതീക്ഷയാണ് | Tilak Varma | NamanDhir",
        "seo_title": "Tilak Varma & Naman Dhir Comeback Analysis | Emerging Cricket Talent",
        "meta_desc": "Tilak Varma's technical comeback and Naman Dhir's explosive potential. Tactical cricket analysis in Malayalam by Haris Nenmara.",
        "published_iso": "2026-10-25T11:02:47+00:00",
        "views": "57K views",
        "read_time": "3 min read",
        "p1_ml": "പരിക്കുകളിൽ നിന്നും ഫോം വീണ്ടെടുക്കലുകളിൽ നിന്നും ശക്തമായി തിരിച്ചെത്തിയ തിലക് വർമ്മയുടെ പ്രകടനവും, യുവതാരം നമൻ ധീർ നൽകുന്ന വലിയ പ്രതീക്ഷകളും ചർച്ച ചെയ്യുന്ന വീഡിയോ. മധ്യനിരയിൽ കളി മുന്നോട്ട് കൊണ്ടുപോകാനുള്ള സാങ്കേതിക മികവും ഡെത്ത് ഓവറുകളിലെ പവർ ഹിറ്റിങ്ങും ഇന്ത്യൻ ക്രിക്കറ്റിന് പുതിയൊരു കരുത്താണ് സമ്മാനിക്കുന്നത്. ഹാരിസ് നെന്മാറയുടെ ആഴത്തിലുള്ള ക്രിക്കറ്റ് വിശകലനം ഇവിടെ കാണാം.",
        "p2_en": "An analytical look at young Indian batting talents Tilak Varma and Naman Dhir. This debrief assesses left-hand right-hand middle-order combinations, shot selection under scoreboard pressure, handling high-speed bouncers, and execution of sweep shots against wrist spin.",
        "takeaways": [
            "Technical adjustments against deliveries angling across the left-hander",
            "Naman Dhir's boundary-hitting leverage and bat swing mechanics",
            "Middle-overs acceleration without losing wicket clusters",
            "Long-term role in Indian white-ball squad transition plans"
        ],
        "tags": ["Tilak Varma", "Naman Dhir", "Team India", "Cricket Talent", "Comeback Analysis", "Haris Nenmara"]
    },
    {
        "id": "3-k7z6FqTX0",
        "slug": "jasprit-bumrah-sanju-samson-ind-vs-wi",
        "sport": "cricket",
        "sport_title": "Cricket Analysis",
        "playlist": "Cricket India",
        "title": "ഭുവി വരുന്നു ! ബുംറ ഇല്ലെങ്കിൽ ഇന്ത്യ ഇല്ലേ ? Sanju Samson | Jasprit Bumrah |Ind Vs Wi",
        "seo_title": "Is India Dependent on Jasprit Bumrah? Bowling Tactics & Match Review",
        "meta_desc": "Is India overly reliant on Jasprit Bumrah? Fast bowling tactics, Bhuvneshwar Kumar, and Sanju Samson discussed by Haris Nenmara.",
        "published_iso": "2026-10-16T11:30:27+00:00",
        "views": "110K views",
        "read_time": "3 min read",
        "p1_ml": "ജസ്പ്രീത് ബുംറ എന്ന ഇതിഹാസ പേസറുടെ അസാന്നിധ്യത്തിൽ ഇന്ത്യൻ ബോളിങ് നിര നേരിടുന്ന വെല്ലുവിളികൾ പരിശോധിക്കുന്ന വീഡിയോ. ഭുവനേശ്വർ കുമാറിന്റെ സ്വിങ് ബോളിങ്ങും പരിചയസമ്പത്തും ഇന്ത്യൻ ടീമിന് എത്രത്തോളം ആവശ്യമാണ്? ഡെത്ത് ഓവറുകളിലെ റൺ ഒഴുക്ക് തടയാൻ ബുംറയെപ്പോലൊരു ബൗളറുടെ വിടവ് എങ്ങനെ നികത്താം എന്ന ചോദ്യത്തിന് ഹാരിസ് നെന്മാറ തന്ത്രപരമായ മറുപടികൾ നൽകുന്നു.",
        "p2_en": "Analyzing Team India's fast-bowling depth and tactical reliance on Jasprit Bumrah. We evaluate yorker precision, release height, reverse swing in subcontinental conditions, and how different bowling combinations perform during powerplay and death-over phases.",
        "takeaways": [
            "Jasprit Bumrah's unique release angle generating late inward seam movement",
            "The value of Bhuvneshwar Kumar's new-ball swing control in the powerplay",
            "Execution of defensive wide yorkers and slower ball variations",
            "Tactical blueprints for India's pace attack across varied international tracks"
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
        "seo_title": "Bhuvneshwar Kumar & Jasprit Bumrah Bowling Synergy | Cricket Tactics",
        "meta_desc": "The lethal bowling partnership: Bhuvneshwar Kumar and Jasprit Bumrah. Powerplay swing meets death-over yorkers. Analysis by Haris Nenmara.",
        "published_iso": "2026-10-17T11:36:23+00:00",
        "views": "21K views",
        "read_time": "3 min read",
        "p1_ml": "ഭുവനേശ്വർ കുമാറിന്റെ കൃത്യതയാർന്ന ന്യൂ-ബോൾ സ്വിംഗും ജസ്പ്രീത് ബുംറയുടെ മാരകമായ യോർക്കറുകളും ഒന്നിച്ചപ്പോൾ ഇന്ത്യൻ ക്രിക്കറ്റ് ആസ്വദിച്ചത് ചരിത്രത്തിലെ ഏറ്റവും മികച്ച ബോളിങ് കൂട്ടുകെട്ടുകളിലൊന്നാണ്. ബാറ്റ്സ്മാൻമാരെ എങ്ങനെയാണ് ഇവർ സമ്മർദ്ദത്തിലാക്കുന്നതെന്നും, രണ്ട് വ്യത്യസ്ത ശൈലികൾ പരസ്പരം പൂരകമായി മാറുന്നത് എങ്ങനെയെന്നും വിശദീകരിക്കുന്ന തന്ത്രപരമായ വീഡിയോ.",
        "p2_en": "A masterclass in bowling synergy: Bhuvneshwar Kumar's swing mastery paired with Jasprit Bumrah's raw pace and yorker accuracy. This debrief studies strike rates, dot-ball percentages, pressure creation from both ends, and why complementary bowling styles are essential for tournament victories.",
        "takeaways": [
            "Complementary bowling styles dismantling opening batting combinations",
            "Dot-ball pressure from one end forcing rash shots at the other",
            "Mastery of seam presentation and wrist position at point of release",
            "Strategic blueprint for modern fast-bowling partnerships"
        ],
        "tags": ["Bhuvneshwar Kumar", "Jasprit Bumrah", "Pace Bowling", "Cricket Partnerships", "India Cricket", "Final Third"]
    }
]

def render_page(video):
    vid = video["id"]
    slug = video["slug"]
    sport = video["sport"]
    url = f"{DOMAIN}/{sport}/{slug}/"
    thumb_hq = f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg"
    thumb_max = f"https://i.ytimg.com/vi/{vid}/maxresdefault.jpg"
    
    # Select related videos from same sport
    related = [v for v in VIDEOS if v["sport"] == sport and v["id"] != vid][:3]
    if len(related) < 3:
        related += [v for v in VIDEOS if v["id"] != vid][:3 - len(related)]
    
    related_cards_html = ""
    for r in related:
        r_url = f"/{r['sport']}/{r['slug']}/"
        related_cards_html += f"""
        <article class="related-card">
          <a href="{r_url}" class="related-thumb-link" aria-label="{r['title']}">
            <img src="https://i.ytimg.com/vi/{r['id']}/hqdefault.jpg" alt="{r['title']}" width="320" height="180" loading="lazy" decoding="async">
            <span class="related-sport-pill">{r['sport'].upper()}</span>
          </a>
          <div class="related-info">
            <span class="related-meta">{r['playlist']} · {r['views']}</span>
            <h3 class="related-title"><a href="{r_url}">{r['title']}</a></h3>
          </div>
        </article>
        """

    takeaways_html = "".join([f"<li>{t}</li>" for t in video["takeaways"]])
    tags_html = "".join([f'<span class="tag-pill">{tag}</span>' for tag in video["tags"]])

    # Breadcrumb schema
    sport_hub_name = "Football Analysis" if sport == "football" else "Cricket Analysis"
    sport_hub_url = f"{DOMAIN}/{sport}/"

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

  <!-- Open Graph / Facebook -->
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

  <!-- Google Tag Manager (Container 1) -->
  <script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
  new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
  j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
  'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
  }})(window,document,'script','dataLayer','GTM-KFC9JGQJ');</script>

  <!-- Google Tag Manager (Container 2) -->
  <script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
  new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
  j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
  'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
  }})(window,document,'script','dataLayer','GTM-5N6XFRJ7');</script>

  <!-- Google Analytics 4 (Async) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-XR8PCQNHRE"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-XR8PCQNHRE');
  </script>

  <!-- Google AdSense -->
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5399554232098923" crossorigin="anonymous"></script>

  <!-- Typography -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Anek+Malayalam:wght@400;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">

  <!-- Schema.org JSON-LD Structured Data -->
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
            "name": "{sport_hub_name}",
            "item": "{sport_hub_url}"
          }},
          {{
            "@type": "ListItem",
            "position": 3,
            "name": {json.dumps(video['seo_title'], ensure_ascii=False)},
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
      --neon-lime-subtle: rgba(158, 226, 11, 0.12);
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

    .navbar {{
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
    .nav-menu {{ display: flex; align-items: center; gap: 1.5rem; list-style: none; }}
    .nav-link {{ color: var(--muted-grey); font-weight: 600; font-size: 0.875rem; transition: color 0.2s; }}
    .nav-link:hover, .nav-link.active {{ color: var(--neon-lime); text-decoration: none; }}

    .breadcrumb-bar {{
      max-width: 1140px;
      margin: 1.5rem auto 0;
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
    .breadcrumb-sep {{ color: var(--dark-grey); }}

    .page-layout {{
      max-width: 1140px;
      margin: 1.5rem auto 5rem;
      padding: 0 1.5rem;
      display: grid;
      grid-template-columns: 1fr 340px;
      gap: 2.5rem;
    }}

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
      padding-top: 56.25%; /* 16:9 Aspect Ratio */
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
      font-size: 1.875rem;
      font-weight: 800;
      line-height: 1.3;
      color: var(--off-white);
      margin-bottom: 1rem;
    }}

    .cta-row {{
      display: flex;
      gap: 0.75rem;
      flex-wrap: wrap;
      margin-top: 1rem;
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
      content: "✓";
      color: var(--neon-lime);
      position: absolute;
      left: 0;
      font-weight: bold;
    }}

    .tags-row {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.5rem;
      margin-top: 1.5rem;
      padding-top: 1.5rem;
      border-top: 1px solid var(--charcoal-border);
    }}

    .tag-pill {{
      background-color: var(--charcoal-light);
      border: 1px solid var(--charcoal-border);
      color: var(--muted-grey);
      font-size: 0.75rem;
      padding: 0.25rem 0.625rem;
      border-radius: 4px;
    }}

    .author-card {{
      background: var(--charcoal);
      border: 1px solid var(--charcoal-border);
      border-radius: 12px;
      padding: 1.5rem;
      display: flex;
      gap: 1.25rem;
      align-items: center;
    }}

    .author-img {{
      width: 72px;
      height: 72px;
      border-radius: 50%;
      object-fit: cover;
      border: 2px solid var(--neon-lime);
      flex-shrink: 0;
    }}

    .author-info h4 {{
      font-size: 1.0625rem;
      font-weight: 700;
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
    }}

    .related-thumb-link {{
      position: relative;
      width: 120px;
      height: 68px;
      flex-shrink: 0;
      border-radius: 6px;
      overflow: hidden;
      background: #000;
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
      background: rgba(0, 0, 0, 0.8);
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
      background-color: var(--pitch-black);
      padding: 3rem 1.5rem;
      color: var(--muted-grey);
      font-size: 0.875rem;
    }}

    .footer-container {{
      max-width: 1140px;
      margin: 0 auto;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 1.5rem;
    }}

    .footer-links {{ display: flex; gap: 1.5rem; list-style: none; }}
    .footer-links a {{ color: var(--muted-grey); font-weight: 600; }}
    .footer-links a:hover {{ color: var(--neon-lime); }}

    @media (max-width: 900px) {{
      .page-layout {{ grid-template-columns: 1fr; }}
      .article-h1 {{ font-size: 1.5rem; }}
      .nav-menu {{ display: none; }}
    }}
  </style>
</head>
<body>

  <!-- Google Tag Manager (noscript fallbacks) -->
  <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-KFC9JGQJ" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
  <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-5N6XFRJ7" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>

  <!-- Navigation -->
  <nav class="navbar" aria-label="Main Navigation">
    <div class="nav-container">
      <a href="/" class="brand-link" aria-label="Final Third Home">
        <img src="/assets/images/final-third-logo.png" alt="Final Third Logo" class="brand-logo" width="160" height="36">
        <span>FINAL THIRD</span>
      </a>
      <ul class="nav-menu">
        <li><a href="/" class="nav-link">Home</a></li>
        <li><a href="/football/" class="nav-link{' active' if sport == 'football' else ''}">Football</a></li>
        <li><a href="/cricket/" class="nav-link{' active' if sport == 'cricket' else ''}">Cricket</a></li>
        <li><a href="/#videos" class="nav-link">Full Catalog (300+)</a></li>
        <li><a href="/#about" class="nav-link">About Haris</a></li>
        <li><a href="/#contact" class="nav-link">Contact</a></li>
      </ul>
    </div>
  </nav>

  <!-- Breadcrumbs -->
  <nav class="breadcrumb-bar" aria-label="Breadcrumb">
    <a href="/">Home</a>
    <span class="breadcrumb-sep">/</span>
    <a href="{sport_hub_url}">{sport_hub_name}</a>
    <span class="breadcrumb-sep">/</span>
    <span style="color: var(--off-white);">{video['slug']}</span>
  </nav>

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
              ← More {video['sport_title']}
            </a>
          </div>
        </div>
      </section>

      <!-- Tactical Editorial Breakdown -->
      <section class="editorial-content">
        <h2>Tactical Breakdown & Match Review | മലയാളം അവലോകനം</h2>
        <p lang="ml">{video['p1_ml']}</p>
        <p>{video['p2_en']}</p>

        <!-- Key Takeaways Box -->
        <div class="takeaways-box">
          <h3>Key Tactical Takeaways & Discussion Points</h3>
          <ul>{takeaways_html}</ul>
        </div>

        <div class="tags-row">
          {tags_html}
        </div>
      </section>

      <!-- Author Attribution Card -->
      <section class="author-card">
        <img src="/assets/images/haris-hero-portrait.png" alt="Haris Nenmara" class="author-img" width="72" height="72" loading="lazy">
        <div class="author-info">
          <h4>Analyzed by Haris Nenmara (ഹാരിസ് നെന്മാറ)</h4>
          <p class="author-role">Sports Journalist & Tactical Analyst · Final Third</p>
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

</body>
</html>
"""
    return html

def render_category_hub(sport):
    sport_name = "Football" if sport == "football" else "Cricket"
    sport_ml = "ഫുട്ബോൾ അവലോകനങ്ങൾ" if sport == "football" else "ക്രിക്കറ്റ് അവലോകനങ്ങൾ"
    meta_desc = (
        "Kerala's premier Malayalam football tactical analysis platform by Haris Nenmara. In-depth match debriefs, El Clasico, Hansi Flick's Barcelona, Real Madrid, and Kerala Blasters ISL breakdowns."
        if sport == "football" else
        "Malayalam cricket match analysis, tactical breakdowns, and player stories by Haris Nenmara. In-depth coverage of Sanju Samson, Jasprit Bumrah, Team India T20s, and World Cup moments."
    )

    vids = [v for v in VIDEOS if v["sport"] == sport]
    
    cards_html = ""
    for v in vids:
        page_url = f"/{sport}/{v['slug']}/"
        cards_html += f"""
        <article class="hub-card">
          <a href="{page_url}" class="hub-card-thumb-link" aria-label="{v['title']}">
            <img src="https://i.ytimg.com/vi/{v['id']}/hqdefault.jpg" alt="{v['title']}" width="480" height="270" loading="lazy">
            <span class="hub-card-badge">{v['playlist']}</span>
            <span class="hub-card-views">{v['views']}</span>
          </a>
          <div class="hub-card-body">
            <span class="hub-card-time">{v['published_iso'][:10]} · {v['read_time']}</span>
            <h2 class="hub-card-title"><a href="{page_url}">{v['title']}</a></h2>
            <p class="hub-card-snippet">{v['meta_desc']}</p>
            <a href="{page_url}" class="hub-card-read-more">Read Tactical Breakdown ↗</a>
          </div>
        </article>
        """

    hub_url = f"{DOMAIN}/{sport}/"

    html = f"""<!DOCTYPE html>
<html lang="en" xml:lang="ml" dir="ltr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{sport_name} Match Analysis & Tactical Debriefs | Final Third with Haris Nenmara</title>
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
      --font-primary: 'Anek Malayalam', 'Inter', sans-serif;
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ background: var(--pitch-black); color: var(--off-white); font-family: var(--font-primary); line-height: 1.6; }}
    a {{ color: var(--neon-lime); text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}

    .navbar {{
      border-bottom: 1px solid var(--charcoal-border);
      background: rgba(8, 8, 8, 0.95);
      position: sticky;
      top: 0;
      z-index: 100;
      padding: 0.875rem 1.5rem;
    }}
    .nav-container {{ max-width: 1140px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; }}
    .brand-link {{ display: flex; align-items: center; gap: 0.75rem; color: var(--off-white); font-weight: 800; font-size: 1.125rem; }}
    .brand-logo {{ height: 36px; width: auto; }}
    .nav-menu {{ display: flex; gap: 1.5rem; list-style: none; }}
    .nav-link {{ color: var(--muted-grey); font-weight: 600; font-size: 0.875rem; }}
    .nav-link:hover, .nav-link.active {{ color: var(--neon-lime); text-decoration: none; }}

    .hub-hero {{
      max-width: 1140px;
      margin: 2rem auto;
      padding: 2.5rem 1.5rem;
      border-bottom: 1px solid var(--charcoal-border);
    }}
    .hub-eyebrow {{ color: var(--neon-lime); font-size: 0.8125rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.5rem; }}
    .hub-title {{ font-size: 2.25rem; font-weight: 800; color: var(--off-white); line-height: 1.2; margin-bottom: 1rem; }}
    .hub-lead {{ font-size: 1.0625rem; color: var(--muted-grey); max-width: 800px; line-height: 1.7; }}

    .hub-grid {{
      max-width: 1140px;
      margin: 2rem auto 5rem;
      padding: 0 1.5rem;
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
      gap: 1.75rem;
    }}

    .hub-card {{
      background: var(--charcoal);
      border: 1px solid var(--charcoal-border);
      border-radius: 12px;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      transition: transform 0.2s, border-color 0.2s;
    }}
    .hub-card:hover {{ transform: translateY(-3px); border-color: rgba(158, 226, 11, 0.4); }}

    .hub-card-thumb-link {{
      position: relative;
      width: 100%;
      padding-top: 56.25%;
      display: block;
      background: #000;
    }}
    .hub-card-thumb-link img {{
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      object-fit: cover;
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
    }}

    .hub-card-body {{ padding: 1.25rem; flex: 1; display: flex; flex-direction: column; }}
    .hub-card-time {{ font-size: 0.75rem; color: var(--dark-grey); margin-bottom: 0.35rem; }}
    .hub-card-title {{ font-size: 1rem; font-weight: 700; line-height: 1.4; margin-bottom: 0.625rem; }}
    .hub-card-title a {{ color: var(--off-white); }}
    .hub-card-title a:hover {{ color: var(--neon-lime); text-decoration: none; }}
    .hub-card-snippet {{ font-size: 0.8125rem; color: var(--muted-grey); line-height: 1.5; margin-bottom: 1rem; flex: 1; }}
    .hub-card-read-more {{ font-size: 0.8125rem; font-weight: 700; color: var(--neon-lime); align-self: flex-start; }}

    .site-footer {{
      border-top: 1px solid var(--charcoal-border);
      background: var(--pitch-black);
      padding: 2.5rem 1.5rem;
      text-align: center;
      color: var(--dark-grey);
      font-size: 0.875rem;
    }}
  </style>
</head>
<body>

  <!-- Navigation -->
  <nav class="navbar">
    <div class="nav-container">
      <a href="/" class="brand-link">
        <img src="/assets/images/final-third-logo.png" alt="Final Third Logo" class="brand-logo" width="160" height="36">
        <span>FINAL THIRD</span>
      </a>
      <ul class="nav-menu">
        <li><a href="/" class="nav-link">Home</a></li>
        <li><a href="/football/" class="nav-link{' active' if sport == 'football' else ''}">Football</a></li>
        <li><a href="/cricket/" class="nav-link{' active' if sport == 'cricket' else ''}">Cricket</a></li>
        <li><a href="/#videos" class="nav-link">Catalog (300+)</a></li>
        <li><a href="/privacy.html" class="nav-link">Privacy</a></li>
        <li><a href="/#contact" class="nav-link">Contact</a></li>
      </ul>
    </div>
  </nav>

  <header class="hub-hero">
    <div class="hub-eyebrow">Category Hub · {sport_ml}</div>
    <h1 class="hub-title">{sport_name} Match Analysis & Tactical Debriefs</h1>
    <p class="hub-lead">{meta_desc}</p>
  </header>

  <main class="hub-grid">
    {cards_html}
  </main>

  <footer class="site-footer">
    <p>&copy; 2026 FINAL THIRD with Haris Nenmara. All rights reserved. · <a href="/">Home</a> · <a href="/privacy.html">Privacy Policy</a></p>
  </footer>

</body>
</html>
"""
    return html

def generate_all():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    
    print("=" * 60)
    print("Final Third — Generating 20 Dedicated Video SEO Pages & Hubs")
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

    # 4. Update index.html cards with crawlable permalinks
    index_path = os.path.join(base_dir, "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        index_html = f.read()

    links_added = 0
    slug_map = {v["id"]: f"/{v['sport']}/{v['slug']}/" for v in VIDEOS}

    for vid, url_path in slug_map.items():
        pattern = rf'(<article class="video-card[^>]*data-video-id="{re.escape(vid)}"[^>]*>.*?</article>)'
        match = re.search(pattern, index_html, re.DOTALL)
        if match:
            card_html = match.group(1)
            if 'class="card-page-link"' not in card_html:
                new_card_html = card_html.replace(
                    '</div>\n          </article>',
                    f'  <div class="card-page-link-row"><a href="{url_path}" class="card-page-link">Read Tactical Breakdown ↗</a></div>\n            </div>\n          </article>'
                )
                if new_card_html != card_html:
                    index_html = index_html[:match.start()] + new_card_html + index_html[match.end():]
                    links_added += 1

    if links_added > 0:
        # Add CSS for card-page-link-row if not present
        if '.card-page-link' not in index_html:
            style_marker = '</style>'
            css_add = """
.card-page-link-row {
  margin-top: 10px;
  padding-top: 8px;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
}
.card-page-link {
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--neon-lime) !important;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  transition: opacity 0.2s;
}
.card-page-link:hover {
  text-decoration: underline !important;
  opacity: 0.85;
}
</style>"""
            index_html = index_html.replace(style_marker, css_add, 1)

        with open(index_path, "w", encoding="utf-8") as f:
            f.write(index_html)
        print(f"✓ Injected crawlable internal links into {links_added} static video cards on homepage!")

if __name__ == "__main__":
    generate_all()
