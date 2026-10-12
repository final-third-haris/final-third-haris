/**
 * FINAL THIRD — Centralized Brand & Content Configuration
 * Official media hub for Final Third with Haris Nenmara.
 * Includes all public videos and playlists from the official YouTube channel.
 */

const FINAL_THIRD_CONFIG = {
  brand: {
    name: "FINAL THIRD",
    tagline: "THE GAME. BEYOND THE OBVIOUS.",
    descriptor: "Football & Cricket Stories, Analysis and Match Coverage",
    malayalamTagline: "കായിക ലോകം, മലയാളത്തിൽ. കഥകൾ സ്കോർബോർഡിനപ്പുറം.",
    description: "Welcome to Final Third, featuring Haris Nenmara. Explore football and cricket videos, match coverage, sports stories, and perspectives on the moments that matter.",
    hostName: "Haris Nenmara",
    accentColor: "#9EE20B", // Official Neon Lime
    colors: {
      neonLime: "#9EE20B",
      pitchBlack: "#080808",
      charcoal: "#151515",
      offWhite: "#F5F5F0",
      mutedGrey: "#A3A3A3"
    },
    logoLime: "assets/images/final-third-logo.png",
    logoWhite: "assets/images/final-third-logo-white.png",
    hostPortrait: "assets/images/haris-host.jpg"
  },

  channel: {
    name: "Final Third with Haris Nenmara",
    handle: "@FinalThird_HarisNenmara",
    url: "https://www.youtube.com/@FinalThird_HarisNenmara"
  },

  contact: {
    phone: "8129059309",
    phoneTel: "+918129059309",
    whatsApp: "8129059309",
    whatsAppLink: "https://wa.me/918129059309",
    email: "mailtofinalthirde@gmail.com",
    emailMailto: "mailto:mailtofinalthirde@gmail.com"
  },

  social: [
    {
      platform: "YouTube",
      handle: "@FinalThird_HarisNenmara",
      url: "https://www.youtube.com/@FinalThird_HarisNenmara",
      description: "Official channel for match reviews, player profiles & breaking coverage.",
      icon: "youtube"
    },
    {
      platform: "Instagram",
      handle: "@finalthird.official",
      url: "https://www.instagram.com/finalthird.official/",
      description: "Matchday reels, behind the scenes, and quick tactical takeaways.",
      icon: "instagram"
    },
    {
      platform: "Facebook",
      handle: "Final Third Official",
      url: "https://www.facebook.com/profile.php?id=61590005744291",
      description: "Malayalam sports community updates and discussion threads.",
      icon: "facebook"
    },
    {
      platform: "WhatsApp Channel",
      handle: "Final Third Updates",
      url: "https://whatsapp.com/channel/0029VbCMhqQ0G0XYaQLOMP2U",
      description: "Instant match alerts, video drops, and Malayalam football headlines.",
      icon: "whatsapp"
    }
  ],

  playlists: {
    football: [
      { id: "kbfc-isl", title: "Kerala Blasters & Indian Football", sport: "football" },
      { id: "PLGWXiMbN17ik", title: "Barcelona", sport: "football" },
      { id: "PLRqJyYpkYUnHsNkojNOoKGYrBITpb_ksS", title: "Real Madrid", sport: "football" },
      { id: "PLRqJyYpkYUnExHY8MwKteSHdDYvAC5MT7", title: "2026 WORLDCUP Stories", sport: "football" },
      { id: "PLRqJyYpkYUnGyLNbCEk8Vdl_Akfdc_h7q", title: "World Cup Previews", sport: "football" }
    ],
    cricket: [
      { id: "PLcWlSk4Ir_yg", title: "Cricket India", sport: "cricket" },
      { id: "PLY1FBwOFOWvQ", title: "India T20", sport: "cricket" },
      { id: "PLRqJyYpkYUnGkQpCzw2M7QRZc-o5dYiGm", title: "IPL Stories", sport: "cricket" }
    ]
  },

  featuredVideoId: "Ustsj3NHM4Y",

  // 100+ Authentic Videos from YouTube @FinalThird_HarisNenmara
  videos: [
  {
    "id": "CriSu9B0l3o",
    "title": "സെനഗലിൽ നിന്നൊരു മാണിക്യം !",
    "sport": "football",
    "playlistId": "kbfc-isl",
    "playlistTitle": "Kerala Blasters & Indian Football",
    "published": "13h ago",
    "views": "1.7K views",
    "summary": "സെനഗലിൽ നിന്നൊരു മാണിക്യം !"
  },
  {
    "id": "ySpbZe77Jgs",
    "title": "ഫാലു ബാക്ക് ; ബ്ലാസ്റ്റേഴ്സ് ബാക്ക് ലൈൻ സുശക്തം | Fallou ndiaye| Kerala Blasters ",
    "sport": "football",
    "playlistId": "kbfc-isl",
    "playlistTitle": "Kerala Blasters & Indian Football",
    "published": "1d ago",
    "views": "28K views",
    "summary": "ഫാലു ബാക്ക് ; ബ്ലാസ്റ്റേഴ്സ് ബാക്ക് ലൈൻ സുശക്തം | Fallou ndiaye| Kerala Blasters "
  },
  {
    "id": "YENti8vmUuw",
    "title": "സഞ്ജു ബാക്ക് ; ഗംഭീർ ഇപ്പോൾ പിച്ചിനെ പഴി പറയുന്നു | Gautam Gambhir | Sanju samson ",
    "sport": "cricket",
    "playlistId": "PLcWlSk4Ir_yg",
    "playlistTitle": "Cricket India",
    "published": "1d ago",
    "views": "67K views",
    "summary": "സഞ്ജു ബാക്ക് ; ഗംഭീർ ഇപ്പോൾ പിച്ചിനെ പഴി പറയുന്നു | Gautam Gambhir | Sanju samson "
  },
  {
    "id": "cOYjZ39qHAU",
    "title": "അറ്റാക്കിൽ യാൻസൺ ; കോട്ട കാക്കാൻ ബോൾട്ടൻ | Kerala Blasters | Momo yansane | James Bolton ",
    "sport": "football",
    "playlistId": "kbfc-isl",
    "playlistTitle": "Kerala Blasters & Indian Football",
    "published": "2d ago",
    "views": "58K views",
    "summary": "അറ്റാക്കിൽ യാൻസൺ ; കോട്ട കാക്കാൻ ബോൾട്ടൻ | Kerala Blasters | Momo yansane | James Bolton "
  },
  {
    "id": "Ustsj3NHM4Y",
    "title": "ബ്ലാസ്റ്റേഴ്സ് മധ്യനിര ഇനി കൊസോവിച്ച് ഭരിക്കും | Kerala Blasters | Nebojša Kosović",
    "sport": "football",
    "playlistId": "kbfc-isl",
    "playlistTitle": "Kerala Blasters & Indian Football",
    "published": "3d ago",
    "views": "86K views",
    "summary": "Detailed tactical breakdown of Kerala Blasters new midfield maestro Nebojša Kosović and how his vision transforms the Manjappada.",
    "featured": true
  },
  {
    "id": "rNiXi4pW9nM",
    "title": "ഇങ്ങനെ ഒരിതിഹാസം ഇനി പിറക്കുമോ ? Lionel Messi | Haris Nenmara ",
    "sport": "football",
    "playlistId": "PLRqJyYpkYUnExHY8MwKteSHdDYvAC5MT7",
    "playlistTitle": "2026 WORLDCUP Stories",
    "published": "4d ago",
    "views": "63K views",
    "summary": "ഇങ്ങനെ ഒരിതിഹാസം ഇനി പിറക്കുമോ ? Lionel Messi | Haris Nenmara "
  },
  {
    "id": "RUtA9Qe6XMk",
    "title": "സനാന്‍ പ്രതീക്ഷയാണ്...ഖാലിദ് ജമീല്‍ പഠിച്ച പാഠങ്ങള്‍ | indian football | Muhammed Sanan",
    "sport": "football",
    "playlistId": "kbfc-isl",
    "playlistTitle": "Kerala Blasters & Indian Football",
    "published": "4d ago",
    "views": "40K views",
    "summary": "സനാന്‍ പ്രതീക്ഷയാണ്...ഖാലിദ് ജമീല്‍ പഠിച്ച പാഠങ്ങള്‍ | indian football | Muhammed Sanan"
  },
  {
    "id": "jcNlAX61XPk",
    "title": "യുഗാന്ത്യം | Messi | Last dance | Argentina | farewell match",
    "sport": "football",
    "playlistId": "PLRqJyYpkYUnExHY8MwKteSHdDYvAC5MT7",
    "playlistTitle": "2026 WORLDCUP Stories",
    "published": "4d ago",
    "views": "14K views",
    "summary": "യുഗാന്ത്യം | Messi | Last dance | Argentina | farewell match"
  },
  {
    "id": "7rU23mHRkVA",
    "title": "വന്നൂ അവർ വന്നൂ | KBFC | MANJAPPADA",
    "sport": "football",
    "playlistId": "kbfc-isl",
    "playlistTitle": "Kerala Blasters & Indian Football",
    "published": "6d ago",
    "views": "4.9K views",
    "summary": "വന്നൂ അവർ വന്നൂ | KBFC | MANJAPPADA"
  },
  {
    "id": "ZuU9k-lVTzE",
    "title": "ആസ്റ്റൺ വില്ലയിൽ നിന്ന് കളി പഠിച്ച ഗ്രീൻ;കൊമ്പന്മാരുടെ പുതിയ സൈനിംഗുകൾ| Kerala Blasters New signings",
    "sport": "football",
    "playlistId": "kbfc-isl",
    "playlistTitle": "Kerala Blasters & Indian Football",
    "published": "6d ago",
    "views": "110K views",
    "summary": "ആസ്റ്റൺ വില്ലയിൽ നിന്ന് കളി പഠിച്ച ഗ്രീൻ;കൊമ്പന്മാരുടെ പുതിയ സൈനിംഗുകൾ| Kerala Blasters New signings"
  },
  {
    "id": "Pm_BM-2fG3w",
    "title": "വൈഭവിനെ പരിഹസിച്ച് സായിം... പ്രതികാരം ഇങ്ങനെ |  | India vs Pakistan",
    "sport": "cricket",
    "playlistId": "PLcWlSk4Ir_yg",
    "playlistTitle": "Cricket India",
    "published": "7d ago",
    "views": "11K views",
    "summary": "വൈഭവിനെ പരിഹസിച്ച് സായിം... പ്രതികാരം ഇങ്ങനെ |  | India vs Pakistan"
  },
  {
    "id": "Kw67lPjMtGg",
    "title": "സഹലിൻ്റെ നട്മഗ് ; വില്യംസിൻ്റെ വേഗപ്പാച്ചിലുകൾ; ഇതാ മാറ്റത്തിൻ്റെ കൊടുങ്കാറ്റ് | | India vs Brazil",
    "sport": "football",
    "playlistId": "kbfc-isl",
    "playlistTitle": "Kerala Blasters & Indian Football",
    "published": "7d ago",
    "views": "13K views",
    "summary": "സഹലിൻ്റെ നട്മഗ് ; വില്യംസിൻ്റെ വേഗപ്പാച്ചിലുകൾ; ഇതാ മാറ്റത്തിൻ്റെ കൊടുങ്കാറ്റ് | | India vs Brazil"
  },
  {
    "id": "DkmNr3Smrbo",
    "title": "പാകിസ്താൻ്റെ ഷോയ്ക്ക് മാത്രം ഒരു കുറവുമില്ല; വൈഭവിനെ തൊട്ടിലാട്ടിയ സായിം | India vs Pakistan ",
    "sport": "cricket",
    "playlistId": "PLcWlSk4Ir_yg",
    "playlistTitle": "Cricket India",
    "published": "7d ago",
    "views": "53K views",
    "summary": "പാകിസ്താൻ്റെ ഷോയ്ക്ക് മാത്രം ഒരു കുറവുമില്ല; വൈഭവിനെ തൊട്ടിലാട്ടിയ സായിം | India vs Pakistan "
  },
  {
    "id": "nkrOAcxX3p0",
    "title": "സഹലിൻ്റെ നട്മഗ് ; വില്യംസിൻ്റെ വേഗപ്പാച്ചിലുകൾ; ഇതാ മാറ്റത്തിൻ്റെ കൊടുങ്കാറ്റ് | | India vs Brazil |",
    "sport": "football",
    "playlistId": "kbfc-isl",
    "playlistTitle": "Kerala Blasters & Indian Football",
    "published": "7d ago",
    "views": "133K views",
    "summary": "സഹലിൻ്റെ നട്മഗ് ; വില്യംസിൻ്റെ വേഗപ്പാച്ചിലുകൾ; ഇതാ മാറ്റത്തിൻ്റെ കൊടുങ്കാറ്റ് | | India vs Brazil |"
  },
  {
    "id": "D_ZzN7VbxMA",
    "title": "എന്താണീ നെഗ്രേറ കേസ്? റഫറിക്ക് പണം കൊടുത്തോ ബാർസ?  പുതിയ തെളിവുമായി റയല്‍| Barcelona | Negreira case",
    "sport": "football",
    "playlistId": "PLGWXiMbN17ik",
    "playlistTitle": "Barcelona",
    "published": "8d ago",
    "views": "19K views",
    "summary": "എന്താണീ നെഗ്രേറ കേസ്? റഫറിക്ക് പണം കൊടുത്തോ ബാർസ?  പുതിയ തെളിവുമായി റയല്‍| Barcelona | Negreira case"
  },
  {
    "id": "timQrwygA-U",
    "title": "ആരെയൊക്കെ വാങ്ങും ? പുതിയ ബ്ലാസ്റ്റേഴ്സ് നല്‍കുന്ന പ്രതീക്ഷകള്‍ | Kerala Blasters | Al fursan group",
    "sport": "football",
    "playlistId": "kbfc-isl",
    "playlistTitle": "Kerala Blasters & Indian Football",
    "published": "9d ago",
    "views": "120K views",
    "summary": "ആരെയൊക്കെ വാങ്ങും ? പുതിയ ബ്ലാസ്റ്റേഴ്സ് നല്‍കുന്ന പ്രതീക്ഷകള്‍ | Kerala Blasters | Al fursan group"
  },
  {
    "id": "dcA3nEqFmZU",
    "title": "400 ഒക്കെ എന്ത്.. അടിച്ച് തൂഫാനാക്കി !",
    "sport": "football",
    "playlistId": "kbfc-isl",
    "playlistTitle": "Kerala Blasters & Indian Football",
    "published": "9d ago",
    "views": "6.5K views",
    "summary": "400 ഒക്കെ എന്ത്.. അടിച്ച് തൂഫാനാക്കി !"
  },
  {
    "id": "_rccklf8LqU",
    "title": "റോണോ യുഗം അവസാനിക്കുന്നു !| | cr7 | portugal",
    "sport": "football",
    "playlistId": "kbfc-isl",
    "playlistTitle": "Kerala Blasters & Indian Football",
    "published": "10d ago",
    "views": "12K views",
    "summary": "റോണോ യുഗം അവസാനിക്കുന്നു !| | cr7 | portugal"
  },
  {
    "id": "mVR_mRYU2YE",
    "title": "കോച്ചോ  റോണോയോ; ആരാണ് ശരി? | Cristiano Ronaldo | Ronaldo Walkout | CR7",
    "sport": "football",
    "playlistId": "PLRqJyYpkYUnExHY8MwKteSHdDYvAC5MT7",
    "playlistTitle": "2026 WORLDCUP Stories",
    "published": "10d ago",
    "views": "108K views",
    "summary": "കോച്ചോ  റോണോയോ; ആരാണ് ശരി? | Cristiano Ronaldo | Ronaldo Walkout | CR7"
  },
  {
    "id": "DiZdqTHFcSQ",
    "title": "ഈ കളി വിദേശ മണ്ണിലും കണ്ടാൽ മതി !| Shubman Gill |  Rohit Sharma IND VS WI |",
    "sport": "cricket",
    "playlistId": "PLcWlSk4Ir_yg",
    "playlistTitle": "Cricket India",
    "published": "10d ago",
    "views": "59K views",
    "summary": "ഈ കളി വിദേശ മണ്ണിലും കണ്ടാൽ മതി !| Shubman Gill |  Rohit Sharma IND VS WI |"
  },
  {
    "id": "yAwrNdTy_jI",
    "title": "കോഹ്‌ലി ഇവിടെയൊക്കെ തന്നെ കാണും | Virat  Kohli | ind vs Wi",
    "sport": "cricket",
    "playlistId": "PLcWlSk4Ir_yg",
    "playlistTitle": "Cricket India",
    "published": "13d ago",
    "views": "69K views",
    "summary": "കോഹ്‌ലി ഇവിടെയൊക്കെ തന്നെ കാണും | Virat  Kohli | ind vs Wi"
  },
  {
    "id": "7GVHR6QA-K4",
    "title": "സിറ്റിയുടെ കപ്പൊക്കെ പോകുമോ ? Man City | EPL ",
    "sport": "football",
    "playlistId": "kbfc-isl",
    "playlistTitle": "Kerala Blasters & Indian Football",
    "published": "2w ago",
    "views": "75K views",
    "summary": "സിറ്റിയുടെ കപ്പൊക്കെ പോകുമോ ? Man City | EPL "
  },
  {
    "id": "IZUaSMWn7qA",
    "title": "ആഷിഖ് കളം നിറഞ്ഞ പോര്; പനാമയെ വിറപ്പിച്ച ഇന്ത്യന്‍ വീരഗാഥ ! | india vs panama | Ryan Williams",
    "sport": "football",
    "playlistId": "kbfc-isl",
    "playlistTitle": "Kerala Blasters & Indian Football",
    "published": "2w ago",
    "views": "107K views",
    "summary": "ആഷിഖ് കളം നിറഞ്ഞ പോര്; പനാമയെ വിറപ്പിച്ച ഇന്ത്യന്‍ വീരഗാഥ ! | india vs panama | Ryan Williams"
  },
  {
    "id": "s0-YkM7wbYo",
    "title": "'സഞ്ജുവിനോട് ഞാനത് തുറന്ന് പറഞ്ഞു '; ഗംഭീറിൻ്റെ വെളിപ്പെടുത്തൽ | Sanju Samson | Gautam Gambhir ",
    "sport": "cricket",
    "playlistId": "PLcWlSk4Ir_yg",
    "playlistTitle": "Cricket India",
    "published": "2w ago",
    "views": "45K views",
    "summary": "'സഞ്ജുവിനോട് ഞാനത് തുറന്ന് പറഞ്ഞു '; ഗംഭീറിൻ്റെ വെളിപ്പെടുത്തൽ | Sanju Samson | Gautam Gambhir "
  },
  {
    "id": "PtEA9Ya7fVE",
    "title": "മോറീന്യോയെ കൊണ്ട് കൂട്ടിയാൽ കൂടില്ലേ? Real Madrid | José Mourinho | kylian mbappé | Vini Jr",
    "sport": "football",
    "playlistId": "PLRqJyYpkYUnHsNkojNOoKGYrBITpb_ksS",
    "playlistTitle": "Real Madrid",
    "published": "2w ago",
    "views": "55K views",
    "summary": "മോറീന്യോയെ കൊണ്ട് കൂട്ടിയാൽ കൂടില്ലേ? Real Madrid | José Mourinho | kylian mbappé | Vini Jr"
  },
  {
    "id": "td_-d4XGhM0",
    "title": "ക്രിക്കറ്റിലും സമുറായി വിപ്ലവം?  ഇന്ത്യയെ വിറപ്പിച്ചു, കയ്യടിച്ച് അയ്യര്‍ | India Vs Japan",
    "sport": "cricket",
    "playlistId": "PLcWlSk4Ir_yg",
    "playlistTitle": "Cricket India",
    "published": "2w ago",
    "views": "71K views",
    "summary": "ക്രിക്കറ്റിലും സമുറായി വിപ്ലവം?  ഇന്ത്യയെ വിറപ്പിച്ചു, കയ്യടിച്ച് അയ്യര്‍ | India Vs Japan"
  },
  {
    "id": "jPVjXRGkpVg",
    "title": "സഞ്ജുവിന്‍റെ സ്ഥിരം വിമര്‍ശകനായ സഹീര്‍ ! Zaheer khan | csk | MS Dhoni | sanju samson",
    "sport": "cricket",
    "playlistId": "PLRqJyYpkYUnGkQpCzw2M7QRZc-o5dYiGm",
    "playlistTitle": "IPL Stories",
    "published": "2w ago",
    "views": "62K views",
    "summary": "സഞ്ജുവിന്‍റെ സ്ഥിരം വിമര്‍ശകനായ സഹീര്‍ ! Zaheer khan | csk | MS Dhoni | sanju samson"
  },
  {
    "id": "Fy_hu6RvvHc",
    "title": "മെസ്സിയുടെ ആ വലിയ റെക്കോർഡ് മറികടക്കുമോ റഫീന്യ ? | Raphinha |  Barcelona ",
    "sport": "football",
    "playlistId": "PLGWXiMbN17ik",
    "playlistTitle": "Barcelona",
    "published": "2w ago",
    "views": "38K views",
    "summary": "മെസ്സിയുടെ ആ വലിയ റെക്കോർഡ് മറികടക്കുമോ റഫീന്യ ? | Raphinha |  Barcelona "
  },
  {
    "id": "9-r2mESOwwo",
    "title": "മിഡിലെ പ്രശ്നം പരിഹരിക്കാതെ റയല്‍ രക്ഷപ്പെടില്ല | real madrid vs atlético madrid",
    "sport": "football",
    "playlistId": "PLRqJyYpkYUnHsNkojNOoKGYrBITpb_ksS",
    "playlistTitle": "Real Madrid",
    "published": "2w ago",
    "views": "57K views",
    "summary": "മിഡിലെ പ്രശ്നം പരിഹരിക്കാതെ റയല്‍ രക്ഷപ്പെടില്ല | real madrid vs atlético madrid"
  },
  {
    "id": "SAninhJhkHw",
    "title": "സഞ്ജു ഇവിടെയൊക്കെ തന്നെ കാണും| sanju samson",
    "sport": "cricket",
    "playlistId": "PLcWlSk4Ir_yg",
    "playlistTitle": "Cricket India",
    "published": "3w ago",
    "views": "8.6K views",
    "summary": "സഞ്ജു ഇവിടെയൊക്കെ തന്നെ കാണും| sanju samson"
  },
  {
    "id": "Hz8sSv--5S8",
    "title": "വൈഭവ് കാത്തിരിക്കണം | Sanju Samson | Abhishek Sharma | IND vs AFG T20 |",
    "sport": "cricket",
    "playlistId": "PLY1FBwOFOWvQ",
    "playlistTitle": "India T20",
    "published": "3w ago",
    "views": "37K views",
    "summary": "വൈഭവ് കാത്തിരിക്കണം | Sanju Samson | Abhishek Sharma | IND vs AFG T20 |"
  },
  {
    "id": "QXb_Y1Vn1ts",
    "title": "സഞ്ജുവിനെ ഇനി വെട്ടില്ല; ഇത് ഗംഭീറിന്‍റെ ഉറപ്പ് | Sanju samson | Gautam Gambhir",
    "sport": "cricket",
    "playlistId": "PLcWlSk4Ir_yg",
    "playlistTitle": "Cricket India",
    "published": "3w ago",
    "views": "166K views",
    "summary": "സഞ്ജുവിനെ ഇനി വെട്ടില്ല; ഇത് ഗംഭീറിന്‍റെ ഉറപ്പ് | Sanju samson | Gautam Gambhir"
  },
  {
    "id": "D49phhFYCi0",
    "title": "എൽ ക്ലാസിക്കോക്ക്  വേണ്ടി കാത്തിരിക്കുന്നു ! | Barcelona | Raphinha | karim adeyemi | Lamine yamal",
    "sport": "football",
    "playlistId": "PLGWXiMbN17ik",
    "playlistTitle": "Barcelona",
    "published": "3w ago",
    "views": "69K views",
    "summary": "എൽ ക്ലാസിക്കോക്ക്  വേണ്ടി കാത്തിരിക്കുന്നു ! | Barcelona | Raphinha | karim adeyemi | Lamine yamal"
  },
  {
    "id": "p83exBjNMnc",
    "title": "വൈഭവിനോട് മത്സരമുണ്ടെന്ന് സഞ്ജു| Sanju Samson | Vaibhav Sooryavanshi",
    "sport": "cricket",
    "playlistId": "PLcWlSk4Ir_yg",
    "playlistTitle": "Cricket India",
    "published": "3w ago",
    "views": "43K views",
    "summary": "വൈഭവിനോട് മത്സരമുണ്ടെന്ന് സഞ്ജു| Sanju Samson | Vaibhav Sooryavanshi"
  },
  {
    "id": "IDB-kIa-Q0w",
    "title": "സഞ്ജു ഇവിടെയൊക്കെ തന്നെ കാണും... | Sanju Samson",
    "sport": "cricket",
    "playlistId": "PLcWlSk4Ir_yg",
    "playlistTitle": "Cricket India",
    "published": "3w ago",
    "views": "19K views",
    "summary": "സഞ്ജു ഇവിടെയൊക്കെ തന്നെ കാണും... | Sanju Samson"
  },
  {
    "id": "GsedMQgKbaE",
    "title": "സഞ്ജുവിനെ വെട്ടാന്‍ കാത്തിരിക്കുന്നവരോട്.. | Sanju Samson | Haris Nenmara",
    "sport": "cricket",
    "playlistId": "PLcWlSk4Ir_yg",
    "playlistTitle": "Cricket India",
    "published": "3w ago",
    "views": "124K views",
    "summary": "സഞ്ജുവിനെ വെട്ടാന്‍ കാത്തിരിക്കുന്നവരോട്.. | Sanju Samson | Haris Nenmara"
  },
  {
    "id": "Ke68-mKP2Qk",
    "title": "സഞ്ജുവിന് കൈഫിൻ്റെ  വിമർശനം! Sanju Samson | Vaibhav Suryavanshi ",
    "sport": "cricket",
    "playlistId": "PLcWlSk4Ir_yg",
    "playlistTitle": "Cricket India",
    "published": "3w ago",
    "views": "35K views",
    "summary": "സഞ്ജുവിന് കൈഫിൻ്റെ  വിമർശനം! Sanju Samson | Vaibhav Suryavanshi "
  },
  {
    "id": "zpUJlZ5vIqQ",
    "title": "എല്ലാം കഴിഞ്ഞ് മാപ്പും കൊണ്ട് വന്നേക്കുന്നു !",
    "sport": "football",
    "playlistId": "kbfc-isl",
    "playlistTitle": "Kerala Blasters & Indian Football",
    "published": "3w ago",
    "views": "2K views",
    "summary": "എല്ലാം കഴിഞ്ഞ് മാപ്പും കൊണ്ട് വന്നേക്കുന്നു !"
  },
  {
    "id": "eSMqm8qT_4w",
    "title": "പത്ത് പേരായ സിറ്റിയോട് യുണൈറ്റഡ് എങ്ങനെ തോറ്റു ? manchester united vs manchester city",
    "sport": "football",
    "playlistId": "kbfc-isl",
    "playlistTitle": "Kerala Blasters & Indian Football",
    "published": "3w ago",
    "views": "47K views",
    "summary": "പത്ത് പേരായ സിറ്റിയോട് യുണൈറ്റഡ് എങ്ങനെ തോറ്റു ? manchester united vs manchester city"
  },
  {
    "id": "SBZaql7Hsp4",
    "title": "സച്ചിനെ എന്ന് കടക്കും റൂട്ട് ? | Joe Root | Sachin Tendulkar  | England",
    "sport": "cricket",
    "playlistId": "PLcWlSk4Ir_yg",
    "playlistTitle": "Cricket India",
    "published": "4w ago",
    "views": "12K views",
    "summary": "സച്ചിനെ എന്ന് കടക്കും റൂട്ട് ? | Joe Root | Sachin Tendulkar  | England"
  },
  {
    "id": "HBt7ZL_oYz0",
    "title": "ജയിച്ചു... പക്ഷേ മോറീന്യോ ഹാപ്പിയല്ല | Real Madrid | Arda Güler",
    "sport": "football",
    "playlistId": "PLRqJyYpkYUnHsNkojNOoKGYrBITpb_ksS",
    "playlistTitle": "Real Madrid",
    "published": "4w ago",
    "views": "32K views",
    "summary": "ജയിച്ചു... പക്ഷേ മോറീന്യോ ഹാപ്പിയല്ല | Real Madrid | Arda Güler"
  },
  {
    "id": "4_3qdMX3Bt4",
    "title": "സഞ്ജുവിനെ നിർബന്ധമായും കളിപ്പിക്കണം എന്ന് മുൻ ഇന്ത്യൻ താരങ്ങൾ | Sanju Samson | India vs Afghanistan",
    "sport": "cricket",
    "playlistId": "PLcWlSk4Ir_yg",
    "playlistTitle": "Cricket India",
    "published": "4w ago",
    "views": "63K views",
    "summary": "സഞ്ജുവിനെ നിർബന്ധമായും കളിപ്പിക്കണം എന്ന് മുൻ ഇന്ത്യൻ താരങ്ങൾ | Sanju Samson | India vs Afghanistan"
  },
  {
    "id": "mQk4-hrx6Zo",
    "title": "ഉറങ്ങിക്കിടക്കുമ്പോള്‍ ടീമിലേക്ക് വിളി വന്നു; പിന്നെയൊക്കെ ചരിത്രം ! |  Razaullah",
    "sport": "football",
    "playlistId": "kbfc-isl",
    "playlistTitle": "Kerala Blasters & Indian Football",
    "published": "4w ago",
    "views": "118K views",
    "summary": "ഉറങ്ങിക്കിടക്കുമ്പോള്‍ ടീമിലേക്ക് വിളി വന്നു; പിന്നെയൊക്കെ ചരിത്രം ! |  Razaullah"
  },
  {
    "id": "ZV7IZEOsxNo",
    "title": "അഗാർക്കറേ.... കണ്ണ് തുറക്ക് | Mohammed Shami | Duleep Trophy ",
    "sport": "football",
    "playlistId": "kbfc-isl",
    "playlistTitle": "Kerala Blasters & Indian Football",
    "published": "1mo ago",
    "views": "36K views",
    "summary": "അഗാർക്കറേ.... കണ്ണ് തുറക്ക് | Mohammed Shami | Duleep Trophy "
  },
  {
    "id": "sHpGWQZ2TpI",
    "title": "റഫീന്യയില്ലാത്ത ബാലന്‍ദ്യോര്‍ ചുരുക്കപ്പട്ടിക | Raphinha",
    "sport": "football",
    "playlistId": "PLGWXiMbN17ik",
    "playlistTitle": "Barcelona",
    "published": "1mo ago",
    "views": "3.5K views",
    "summary": "റഫീന്യയില്ലാത്ത ബാലന്‍ദ്യോര്‍ ചുരുക്കപ്പട്ടിക | Raphinha"
  },
  {
    "id": "cdNZvpx1vN4",
    "title": "റഫീന്യ രണ്ടും കല്‍പ്പിച്ചാണ്... ബാഴ്സയും | Raphinha | Barcelona | UCL",
    "sport": "football",
    "playlistId": "PLGWXiMbN17ik",
    "playlistTitle": "Barcelona",
    "published": "1mo ago",
    "views": "50K views",
    "summary": "റഫീന്യ രണ്ടും കല്‍പ്പിച്ചാണ്... ബാഴ്സയും | Raphinha | Barcelona | UCL"
  },
  {
    "id": "c85MNXGqUxg",
    "title": "ആര് തൂക്കും ബാലൻദ്യോർ ?|  ballon d'or | Lamine Yamal | Harry kane | Lionel Messi | Rodri",
    "sport": "football",
    "playlistId": "PLGWXiMbN17ik",
    "playlistTitle": "Barcelona",
    "published": "1mo ago",
    "views": "26K views",
    "summary": "ആര് തൂക്കും ബാലൻദ്യോർ ?|  ballon d'or | Lamine Yamal | Harry kane | Lionel Messi | Rodri"
  },
  {
    "id": "uTTwCrRqVtY",
    "title": "ജയിച്ചിട്ടും കാണികൾ കൂവുന്ന റയൽ ; പഠിക്കാനുണ്ട് ഇനിയുമേറെ  | Real Madrid vs Inter Milan | Ucl |",
    "sport": "football",
    "playlistId": "PLRqJyYpkYUnHsNkojNOoKGYrBITpb_ksS",
    "playlistTitle": "Real Madrid",
    "published": "1mo ago",
    "views": "37K views",
    "summary": "ജയിച്ചിട്ടും കാണികൾ കൂവുന്ന റയൽ ; പഠിക്കാനുണ്ട് ഇനിയുമേറെ  | Real Madrid vs Inter Milan | Ucl |"
  },
  {
    "id": "ZmW5I7nZSZc",
    "title": "റയലേ... ഒരുങ്ങിയിരുന്നോ, ബാഴ്സയുമായുള്ള അങ്കത്തിന് | Barcelona | Raphinha | Fermin Lopez | Yamal",
    "sport": "football",
    "playlistId": "PLGWXiMbN17ik",
    "playlistTitle": "Barcelona",
    "published": "1mo ago",
    "views": "61K views",
    "summary": "റയലേ... ഒരുങ്ങിയിരുന്നോ, ബാഴ്സയുമായുള്ള അങ്കത്തിന് | Barcelona | Raphinha | Fermin Lopez | Yamal"
  },
  {
    "id": "M9LIu0SkvRs",
    "title": "ഒഡഗാര്‍ഡ് നിറയുന്നു; ഇത് ഗണ്ണേഴ്സിന്‍റെ റെമോന്‍ടാഡ | Arsenal vs Chelsea | martin odegaard",
    "sport": "football",
    "playlistId": "kbfc-isl",
    "playlistTitle": "Kerala Blasters & Indian Football",
    "published": "1mo ago",
    "views": "1.1K views",
    "summary": "ഒഡഗാര്‍ഡ് നിറയുന്നു; ഇത് ഗണ്ണേഴ്സിന്‍റെ റെമോന്‍ടാഡ | Arsenal vs Chelsea | martin odegaard"
  },
  {
    "id": "nj9a6S8bNu4",
    "title": "ഒഡഗാര്‍ഡ് നിറയുന്നു; ഒപ്പം ഹാവേട്ട്സും സോളിസും| Arsenal vs Chelsea | martin odegaard",
    "sport": "football",
    "playlistId": "kbfc-isl",
    "playlistTitle": "Kerala Blasters & Indian Football",
    "published": "1mo ago",
    "views": "25K views",
    "summary": "ഒഡഗാര്‍ഡ് നിറയുന്നു; ഒപ്പം ഹാവേട്ട്സും സോളിസും| Arsenal vs Chelsea | martin odegaard"
  },
  {
    "id": "aNFVC9dITg0",
    "title": "അമ്പോ ഇതെന്തൊരു സെഞ്ചുറി ! വൈഭവിനൊപ്പം കളം നിറയാൻ ലുവാൻ | Lhuan-dre Pretorius",
    "sport": "football",
    "playlistId": "kbfc-isl",
    "playlistTitle": "Kerala Blasters & Indian Football",
    "published": "1mo ago",
    "views": "19K views",
    "summary": "അമ്പോ ഇതെന്തൊരു സെഞ്ചുറി ! വൈഭവിനൊപ്പം കളം നിറയാൻ ലുവാൻ | Lhuan-dre Pretorius"
  },
  {
    "id": "TvTDFoFYLhY",
    "title": "മോറീന്യോ ഉത്തരം കണ്ടെത്തേണ്ട ചോദ്യങ്ങൾ |  Real Madrid | Jose Mourinho ",
    "sport": "football",
    "playlistId": "PLRqJyYpkYUnHsNkojNOoKGYrBITpb_ksS",
    "playlistTitle": "Real Madrid",
    "published": "1mo ago",
    "views": "49K views",
    "summary": "മോറീന്യോ ഉത്തരം കണ്ടെത്തേണ്ട ചോദ്യങ്ങൾ |  Real Madrid | Jose Mourinho "
  },
  {
    "id": "UDTM2RdwGtQ",
    "title": "റിവ്യൂ മീറ്റിംഗിൽ ചർച്ചയായത്  | Rohit Sharma | Virat Kohli |  2027 World Cup | ODI | BCCI",
    "sport": "cricket",
    "playlistId": "PLcWlSk4Ir_yg",
    "playlistTitle": "Cricket India",
    "published": "1mo ago",
    "views": "25K views",
    "summary": "റിവ്യൂ മീറ്റിംഗിൽ ചർച്ചയായത്  | Rohit Sharma | Virat Kohli |  2027 World Cup | ODI | BCCI"
  },
  {
    "id": "UsCSX9iGrS8",
    "title": "മെസി മോറീന്യോയെ ഉറക്കിയ രാത്രി | Lionel Messi",
    "sport": "football",
    "playlistId": "PLRqJyYpkYUnExHY8MwKteSHdDYvAC5MT7",
    "playlistTitle": "2026 WORLDCUP Stories",
    "published": "1mo ago",
    "views": "1.4K views",
    "summary": "മെസി മോറീന്യോയെ ഉറക്കിയ രാത്രി | Lionel Messi"
  },
  {
    "id": "TCVU4HhLDfg",
    "title": "ഗോര്‍ഡന്‍ നിറയുന്ന ബാഴ്സ | Anthony Gordon",
    "sport": "football",
    "playlistId": "kbfc-isl",
    "playlistTitle": "Kerala Blasters & Indian Football",
    "published": "1mo ago",
    "views": "2.3K views",
    "summary": "ഗോര്‍ഡന്‍ നിറയുന്ന ബാഴ്സ | Anthony Gordon"
  },
  {
    "id": "tA_VV_BgHJI",
    "title": "ലിയോ ക്രിസ്റ്റ്യാനോക്ക് സമ്മാനിച്ച ഉണങ്ങാ മുറിവ് | Barcelona | Real Madrid | LionelMessi",
    "sport": "football",
    "playlistId": "PLGWXiMbN17ik",
    "playlistTitle": "Barcelona",
    "published": "1mo ago",
    "views": "53K views",
    "summary": "ലിയോ ക്രിസ്റ്റ്യാനോക്ക് സമ്മാനിച്ച ഉണങ്ങാ മുറിവ് | Barcelona | Real Madrid | LionelMessi"
  },
  {
    "id": "7zRWY5bg-ns",
    "title": "പരിക്കേറ്റവരെ കുത്തി നിറച്ചൊരു ടീം എന്തിനാണ് ? Sanju Samson | vaibhav sooryavanshi",
    "sport": "cricket",
    "playlistId": "PLcWlSk4Ir_yg",
    "playlistTitle": "Cricket India",
    "published": "1mo ago",
    "views": "45K views",
    "summary": "പരിക്കേറ്റവരെ കുത്തി നിറച്ചൊരു ടീം എന്തിനാണ് ? Sanju Samson | vaibhav sooryavanshi"
  },
  {
    "id": "xxTItNSRkgI",
    "title": "യമാൽ ബാക്ക്; ഗോഡൻ നൽകുന്ന പ്രതീക്ഷകൾ | Anthony Gordon | Barcelona ",
    "sport": "football",
    "playlistId": "PLGWXiMbN17ik",
    "playlistTitle": "Barcelona",
    "published": "1mo ago",
    "views": "66K views",
    "summary": "യമാൽ ബാക്ക്; ഗോഡൻ നൽകുന്ന പ്രതീക്ഷകൾ | Anthony Gordon | Barcelona "
  },
  {
    "id": "WM8nn7CtAO4",
    "title": "ഇമാമിൻ്റെ അഭിനയം , അടപടലം തോൽവികൾ , എന്തൊക്കെയാ ഈ നടക്കുന്നേ... | Pakistan Cricket",
    "sport": "cricket",
    "playlistId": "PLcWlSk4Ir_yg",
    "playlistTitle": "Cricket India",
    "published": "1mo ago",
    "views": "14K views",
    "summary": "ഇമാമിൻ്റെ അഭിനയം , അടപടലം തോൽവികൾ , എന്തൊക്കെയാ ഈ നടക്കുന്നേ... | Pakistan Cricket"
  },
  {
    "id": "Ba3xWB-ECSA",
    "title": "മെസി ഈ മൈതാനങ്ങളില്‍ ബാക്കിയാക്കുന്നത്...| Lionel Messi | Haris Nenmara",
    "sport": "football",
    "playlistId": "PLRqJyYpkYUnExHY8MwKteSHdDYvAC5MT7",
    "playlistTitle": "2026 WORLDCUP Stories",
    "published": "1mo ago",
    "views": "16K views",
    "summary": "മെസി ഈ മൈതാനങ്ങളില്‍ ബാക്കിയാക്കുന്നത്...| Lionel Messi | Haris Nenmara"
  },
  {
    "id": "2agTk0JVYnQ",
    "title": "അരങ്ങേറ്റത്തില്‍ റെഡ് കാര്‍ഡ് കണ്ട മെസി.. പിന്നെയൊക്കെ ചരിത്രം ! Lionel Messi | Haris Nenmara",
    "sport": "football",
    "playlistId": "PLRqJyYpkYUnExHY8MwKteSHdDYvAC5MT7",
    "playlistTitle": "2026 WORLDCUP Stories",
    "published": "1mo ago",
    "views": "88K views",
    "summary": "അരങ്ങേറ്റത്തില്‍ റെഡ് കാര്‍ഡ് കണ്ട മെസി.. പിന്നെയൊക്കെ ചരിത്രം ! Lionel Messi | Haris Nenmara"
  },
  {
    "id": "m_cPMk1VEhk",
    "title": "മൗറിഞ്ഞോ പെപ്പിനെ വീഴ്ത്തിയ രാത്രി  | Haris Nenmara | Final Third",
    "sport": "football",
    "playlistId": "kbfc-isl",
    "playlistTitle": "Kerala Blasters & Indian Football",
    "published": "1mo ago",
    "views": "6.4K views",
    "summary": "മൗറിഞ്ഞോ പെപ്പിനെ വീഴ്ത്തിയ രാത്രി  | Haris Nenmara | Final Third"
  },
  {
    "id": "6f8J5SJ43J4",
    "title": "അവസാന മണിക്കൂറുകളിൽ പാചകം തുടരുന്ന ഡെക്കോ| Gabriel Jesus | Barcelona | Deco",
    "sport": "football",
    "playlistId": "PLGWXiMbN17ik",
    "playlistTitle": "Barcelona",
    "published": "1mo ago",
    "views": "63K views",
    "summary": "അവസാന മണിക്കൂറുകളിൽ പാചകം തുടരുന്ന ഡെക്കോ| Gabriel Jesus | Barcelona | Deco"
  },
  {
    "id": "JxcAV33OSd0",
    "title": "മോറീന്യോ എല്ലാം തിരിച്ച് പിടിച്ച് തുടങ്ങുന്നു ! Jude Bellingham | Real madrid",
    "sport": "football",
    "playlistId": "PLRqJyYpkYUnHsNkojNOoKGYrBITpb_ksS",
    "playlistTitle": "Real Madrid",
    "published": "1mo ago",
    "views": "49K views",
    "summary": "മോറീന്യോ എല്ലാം തിരിച്ച് പിടിച്ച് തുടങ്ങുന്നു ! Jude Bellingham | Real madrid"
  },
  {
    "id": "izQ2wqMHjrE",
    "title": "മോറീന്യോ ടിക്കി ടാക്കയെ ചോദ്യ മുനയിൽ നിർത്തിയ രാത്രി | Jose mourinho  | cristiano Ronaldo",
    "sport": "football",
    "playlistId": "PLRqJyYpkYUnHsNkojNOoKGYrBITpb_ksS",
    "playlistTitle": "Real Madrid",
    "published": "1mo ago",
    "views": "54K views",
    "summary": "മോറീന്യോ ടിക്കി ടാക്കയെ ചോദ്യ മുനയിൽ നിർത്തിയ രാത്രി | Jose mourinho  | cristiano Ronaldo"
  },
  {
    "id": "6d-0gDVk1Mw",
    "title": "സഞ്ജു അന്ന് പറഞ്ഞത് , തന്നെ വെട്ടിയതിൽ സ്കൈയുടെ അമർഷം| Sanju Samson| Surya Kumar Yadav",
    "sport": "cricket",
    "playlistId": "PLcWlSk4Ir_yg",
    "playlistTitle": "Cricket India",
    "published": "1mo ago",
    "views": "239K views",
    "summary": "സഞ്ജു അന്ന് പറഞ്ഞത് , തന്നെ വെട്ടിയതിൽ സ്കൈയുടെ അമർഷം| Sanju Samson| Surya Kumar Yadav"
  },
  {
    "id": "cYdif52eHCU",
    "title": "ബാഴ്സ വിയർക്കും; ഗണ്ണേഴ്‌സിനോട് പകരം ചോദിക്കാൻ റയൽ | Barcelona| Real Madrid| UCL",
    "sport": "football",
    "playlistId": "PLGWXiMbN17ik",
    "playlistTitle": "Barcelona",
    "published": "1mo ago",
    "views": "47K views",
    "summary": "ബാഴ്സ വിയർക്കും; ഗണ്ണേഴ്‌സിനോട് പകരം ചോദിക്കാൻ റയൽ | Barcelona| Real Madrid| UCL"
  },
  {
    "id": "cJHqobdG-1c",
    "title": "എൻസോ കൂടെ വന്നാൽ കഥ മാറും | Rayan Cherki  | Erling Haaland | Manchester City",
    "sport": "football",
    "playlistId": "kbfc-isl",
    "playlistTitle": "Kerala Blasters & Indian Football",
    "published": "1mo ago",
    "views": "29K views",
    "summary": "എൻസോ കൂടെ വന്നാൽ കഥ മാറും | Rayan Cherki  | Erling Haaland | Manchester City"
  },
  {
    "id": "17Pa0lQIGx0",
    "title": "സിറാജ് എന്ന ടീം മാൻ.. Mohammed Siraj",
    "sport": "football",
    "playlistId": "kbfc-isl",
    "playlistTitle": "Kerala Blasters & Indian Football",
    "published": "1mo ago",
    "views": "2.7K views",
    "summary": "സിറാജ് എന്ന ടീം മാൻ.. Mohammed Siraj"
  },
  {
    "id": "O6u3djLzaJ0",
    "title": "പറഞ്ഞ് വിടടേ...| Julian Alvarez",
    "sport": "football",
    "playlistId": "kbfc-isl",
    "playlistTitle": "Kerala Blasters & Indian Football",
    "published": "1mo ago",
    "views": "4.4K views",
    "summary": "പറഞ്ഞ് വിടടേ...| Julian Alvarez"
  },
  {
    "id": "AIAW1N_zlLo",
    "title": "അല്‍വാരസിനെ അത്ലറ്റിക്കോ ഇനിയും ഇങ്ങനെ പിടിച്ച് നിര്‍ത്തുന്നത് എന്തിനാണ് |  julian alvarez",
    "sport": "football",
    "playlistId": "kbfc-isl",
    "playlistTitle": "Kerala Blasters & Indian Football",
    "published": "1mo ago",
    "views": "13K views",
    "summary": "അല്‍വാരസിനെ അത്ലറ്റിക്കോ ഇനിയും ഇങ്ങനെ പിടിച്ച് നിര്‍ത്തുന്നത് എന്തിനാണ് |  julian alvarez"
  },
  {
    "id": "O4ToLj6B35M",
    "title": "സിറാജാണോ സെഞ്ച്വറിയടിച്ചത് ! അയാള്‍ ഇങ്ങനെയൊക്കെയാണ് | Mohammed Siraj | Dhruv Jurel",
    "sport": "football",
    "playlistId": "kbfc-isl",
    "playlistTitle": "Kerala Blasters & Indian Football",
    "published": "1mo ago",
    "views": "24K views",
    "summary": "സിറാജാണോ സെഞ്ച്വറിയടിച്ചത് ! അയാള്‍ ഇങ്ങനെയൊക്കെയാണ് | Mohammed Siraj | Dhruv Jurel"
  },
  {
    "id": "-kFphDKA8Fs",
    "title": "സിറാജ് തന്‍റേതെന്ന പോലെ ആഘോഷിച്ച സെഞ്ച്വറികള്‍ | Mohammed Siraj | Dhruv Jurel",
    "sport": "football",
    "playlistId": "kbfc-isl",
    "playlistTitle": "Kerala Blasters & Indian Football",
    "published": "1mo ago",
    "views": "40K views",
    "summary": "സിറാജ് തന്‍റേതെന്ന പോലെ ആഘോഷിച്ച സെഞ്ച്വറികള്‍ | Mohammed Siraj | Dhruv Jurel"
  },
  {
    "id": "QSS6VTsBQUg",
    "title": "ബാഴ്സക്ക് തരില്ല ! നിലപാടിൽ മാറ്റമില്ലാതെ അത്ലറ്റിക്കോ| Julian Alvarez | Atletico Madrid | Barcelona",
    "sport": "football",
    "playlistId": "PLGWXiMbN17ik",
    "playlistTitle": "Barcelona",
    "published": "1mo ago",
    "views": "41K views",
    "summary": "ബാഴ്സക്ക് തരില്ല ! നിലപാടിൽ മാറ്റമില്ലാതെ അത്ലറ്റിക്കോ| Julian Alvarez | Atletico Madrid | Barcelona"
  },
  {
    "id": "hsRQP30xBdA",
    "title": "ജയ്സ്വാളിന് ICC യുടെ എട്ടിന്‍റെ പണി വരുന്നുണ്ട് ?  Yashasvi Jaiswal | ICC",
    "sport": "football",
    "playlistId": "kbfc-isl",
    "playlistTitle": "Kerala Blasters & Indian Football",
    "published": "1mo ago",
    "views": "11K views",
    "summary": "ജയ്സ്വാളിന് ICC യുടെ എട്ടിന്‍റെ പണി വരുന്നുണ്ട് ?  Yashasvi Jaiswal | ICC"
  },
  {
    "id": "jYaYoQotDyc",
    "title": "എസ്പിയെ വെറുതെ തൂക്കിയതല്ല ! | Haris Nenmara | Final Third",
    "sport": "football",
    "playlistId": "kbfc-isl",
    "playlistTitle": "Kerala Blasters & Indian Football",
    "published": "1mo ago",
    "views": "6.5K views",
    "summary": "എസ്പിയെ വെറുതെ തൂക്കിയതല്ല ! | Haris Nenmara | Final Third"
  },
  {
    "id": "To36_SUc0zY",
    "title": "ജൂഡും ഗുളറും കളം നിറയുന്നു... റയൽ ഇനിയും പഠിക്കാനുണ്ട് ! Real Madrid | Carlos Espi ",
    "sport": "football",
    "playlistId": "PLRqJyYpkYUnHsNkojNOoKGYrBITpb_ksS",
    "playlistTitle": "Real Madrid",
    "published": "1mo ago",
    "views": "21K views",
    "summary": "ജൂഡും ഗുളറും കളം നിറയുന്നു... റയൽ ഇനിയും പഠിക്കാനുണ്ട് ! Real Madrid | Carlos Espi "
  },
  {
    "id": "_rhxQ3hov10",
    "title": "സ്റ്റാർക്കിന്റെ പ്രതികാരം  |",
    "sport": "football",
    "playlistId": "kbfc-isl",
    "playlistTitle": "Kerala Blasters & Indian Football",
    "published": "1mo ago",
    "views": "34K views",
    "summary": "സ്റ്റാർക്കിന്റെ പ്രതികാരം  |"
  },
  {
    "id": "LOzGOjUa8As",
    "title": "ലോകകപ്പിന് ഈ ടീം സെറ്റാണ് ! Sanju Samson | Vaibhav suryavanshi | Haris Nenmara",
    "sport": "cricket",
    "playlistId": "PLcWlSk4Ir_yg",
    "playlistTitle": "Cricket India",
    "published": "1mo ago",
    "views": "23K views",
    "summary": "ലോകകപ്പിന് ഈ ടീം സെറ്റാണ് ! Sanju Samson | Vaibhav suryavanshi | Haris Nenmara"
  },
  {
    "id": "e4LY06WzjPo",
    "title": "22 പന്തിൽ സ്റ്റാർക്കിന്റെ  ബംഗ്ലാദേശ് വധം | Mitchell Starc | Bangladesh | AUS vs BAN 2nd Test",
    "sport": "football",
    "playlistId": "kbfc-isl",
    "playlistTitle": "Kerala Blasters & Indian Football",
    "published": "1mo ago",
    "views": "29K views",
    "summary": "22 പന്തിൽ സ്റ്റാർക്കിന്റെ  ബംഗ്ലാദേശ് വധം | Mitchell Starc | Bangladesh | AUS vs BAN 2nd Test"
  },
  {
    "id": "Yd1Kt1LEYV0",
    "title": "പരെഡസിന് കിട്ടേണ്ടത് തന്നെ | Leandro Paredes | Argentina| Fifa | World Cup",
    "sport": "football",
    "playlistId": "PLRqJyYpkYUnExHY8MwKteSHdDYvAC5MT7",
    "playlistTitle": "2026 WORLDCUP Stories",
    "published": "1mo ago",
    "views": "16K views",
    "summary": "പരെഡസിന് കിട്ടേണ്ടത് തന്നെ | Leandro Paredes | Argentina| Fifa | World Cup"
  },
  {
    "id": "anbguWekVD0",
    "title": "ലോകകപ്പിന്  ഈ ടീം സെറ്റാണ് !  Sanju Samson | Vaibhav suryavanshi | Haris Nenmara ",
    "sport": "cricket",
    "playlistId": "PLcWlSk4Ir_yg",
    "playlistTitle": "Cricket India",
    "published": "1mo ago",
    "views": "16K views",
    "summary": "ലോകകപ്പിന്  ഈ ടീം സെറ്റാണ് !  Sanju Samson | Vaibhav suryavanshi | Haris Nenmara "
  },
  {
    "id": "TuLduMsLUXw",
    "title": "അല്‍വാരസ് വരില്ല... ഹംസയെ അവതരിപ്പിക്കുമോ ഫ്ലിക്ക് ! Hamza Abdelkarim | Barcelona",
    "sport": "football",
    "playlistId": "PLGWXiMbN17ik",
    "playlistTitle": "Barcelona",
    "published": "1mo ago",
    "views": "23K views",
    "summary": "അല്‍വാരസ് വരില്ല... ഹംസയെ അവതരിപ്പിക്കുമോ ഫ്ലിക്ക് ! Hamza Abdelkarim | Barcelona"
  },
  {
    "id": "l8oDE6NmkNM",
    "title": "പന്തിൻ്റെ കംബാക്ക് ; ടെസ്റ്റ് ചാംപ്യൻഷിപ്പ് പ്രതീക്ഷകൾ ! india vs Srilanka ",
    "sport": "football",
    "playlistId": "kbfc-isl",
    "playlistTitle": "Kerala Blasters & Indian Football",
    "published": "1mo ago",
    "views": "10K views",
    "summary": "പന്തിൻ്റെ കംബാക്ക് ; ടെസ്റ്റ് ചാംപ്യൻഷിപ്പ് പ്രതീക്ഷകൾ ! india vs Srilanka "
  },
  {
    "id": "hftMTk-0da4",
    "title": "ബലേബ വരും;  ഈ സ്ക്വാഡ് മതിയോ യുണൈറ്റഡിന് ? | Manchester United Season Preview",
    "sport": "football",
    "playlistId": "kbfc-isl",
    "playlistTitle": "Kerala Blasters & Indian Football",
    "published": "1mo ago",
    "views": "19K views",
    "summary": "ബലേബ വരും;  ഈ സ്ക്വാഡ് മതിയോ യുണൈറ്റഡിന് ? | Manchester United Season Preview"
  },
  {
    "id": "LWaRbgu39CE",
    "title": "ബാഴ്‌സയെ ഇനി പിടിച്ചാൽ കിട്ടില്ല | Haris Nenmara | barcelona | rodri |",
    "sport": "football",
    "playlistId": "PLGWXiMbN17ik",
    "playlistTitle": "Barcelona",
    "published": "1mo ago",
    "views": "25K views",
    "summary": "ബാഴ്‌സയെ ഇനി പിടിച്ചാൽ കിട്ടില്ല | Haris Nenmara | barcelona | rodri |"
  },
  {
    "id": "83gdN3Y9LOQ",
    "title": "ഇക്കുറി ചാമ്പ്യൻസ് ലീഗും തൂക്കും ! | Rodri  | Barcelona | Joao Cancelo | Transfers | La Liga | Ucl",
    "sport": "football",
    "playlistId": "PLGWXiMbN17ik",
    "playlistTitle": "Barcelona",
    "published": "1mo ago",
    "views": "36K views",
    "summary": "ഇക്കുറി ചാമ്പ്യൻസ് ലീഗും തൂക്കും ! | Rodri  | Barcelona | Joao Cancelo | Transfers | La Liga | Ucl"
  },
  {
    "id": "LjW-5wR0oXk",
    "title": "മോറീന്യോയുടെ ഉള്ളില്‍ ഇപ്പോഴും ആ പഴയ വീറുണ്ടോ? jose mourinho",
    "sport": "football",
    "playlistId": "PLRqJyYpkYUnHsNkojNOoKGYrBITpb_ksS",
    "playlistTitle": "Real Madrid",
    "published": "1mo ago",
    "views": "3.9K views",
    "summary": "മോറീന്യോയുടെ ഉള്ളില്‍ ഇപ്പോഴും ആ പഴയ വീറുണ്ടോ? jose mourinho"
  },
  {
    "id": "B1jFnZiQVk8",
    "title": "മോറീന്യോ റയലിനെ രക്ഷിക്കുമോ? | jose mourinho | Haris Nenmara",
    "sport": "football",
    "playlistId": "PLRqJyYpkYUnHsNkojNOoKGYrBITpb_ksS",
    "playlistTitle": "Real Madrid",
    "published": "1mo ago",
    "views": "1.1K views",
    "summary": "മോറീന്യോ റയലിനെ രക്ഷിക്കുമോ? | jose mourinho | Haris Nenmara"
  },
  {
    "id": "ajCEM-uJbD0",
    "title": "സായ് വരുന്നത് വരെയേ പടിക്കലിന് ആയുസ്സുള്ളൂ എന്നാണോ ? | Yashasvi Jaiswal | KL Rahul | IND vs SL",
    "sport": "cricket",
    "playlistId": "PLcWlSk4Ir_yg",
    "playlistTitle": "Cricket India",
    "published": "1mo ago",
    "views": "10K views",
    "summary": "സായ് വരുന്നത് വരെയേ പടിക്കലിന് ആയുസ്സുള്ളൂ എന്നാണോ ? | Yashasvi Jaiswal | KL Rahul | IND vs SL"
  },
  {
    "id": "3ifhhcQXYOo",
    "title": "ഓസീസിന്റെ  നെഞ്ചത്ത് കടുവകളുടെ നാഗിൻ ഡാൻസ് | Australia vs Bangladesh | Mehidy Hasan  Test Highlights",
    "sport": "football",
    "playlistId": "kbfc-isl",
    "playlistTitle": "Kerala Blasters & Indian Football",
    "published": "1mo ago",
    "views": "20K views",
    "summary": "ഓസീസിന്റെ  നെഞ്ചത്ത് കടുവകളുടെ നാഗിൻ ഡാൻസ് | Australia vs Bangladesh | Mehidy Hasan  Test Highlights"
  },
  {
    "id": "EFiPLaBLQbc",
    "title": " സ്റ്റാർക്കിന്റെ ഫ്രസ്ട്രേഷൻ മനസിലാകും ! | Australia vs Bangladesh | Haris Nenmara ",
    "sport": "football",
    "playlistId": "kbfc-isl",
    "playlistTitle": "Kerala Blasters & Indian Football",
    "published": "1mo ago",
    "views": "51K views",
    "summary": " സ്റ്റാർക്കിന്റെ ഫ്രസ്ട്രേഷൻ മനസിലാകും ! | Australia vs Bangladesh | Haris Nenmara "
  },
  {
    "id": "NdacMNo-Rg0",
    "title": "ബാഴ്സയെ വെല്ലാനുള്ള സ്ക്വാഡുണ്ടോ റയലിന്?| Jose mourinho | Real Madrid | Haris Nenmara",
    "sport": "football",
    "playlistId": "PLRqJyYpkYUnHsNkojNOoKGYrBITpb_ksS",
    "playlistTitle": "Real Madrid",
    "published": "1mo ago",
    "views": "30K views",
    "summary": "ബാഴ്സയെ വെല്ലാനുള്ള സ്ക്വാഡുണ്ടോ റയലിന്?| Jose mourinho | Real Madrid | Haris Nenmara"
  },
  {
    "id": "dDvMTma4i38",
    "title": "ആ സെഞ്ചുറി വലിയൊരു സിഗ്നലാണ് | Rocky Flintoff Century | Andrew Flintoff | Haris Nenmara | England",
    "sport": "football",
    "playlistId": "kbfc-isl",
    "playlistTitle": "Kerala Blasters & Indian Football",
    "published": "1mo ago",
    "views": "5.5K views",
    "summary": "ആ സെഞ്ചുറി വലിയൊരു സിഗ്നലാണ് | Rocky Flintoff Century | Andrew Flintoff | Haris Nenmara | England"
  },
  {
    "id": "nq-bu8QAdKc",
    "title": "ലോക ടെസ്റ്റ് ചാമ്പ്യന്‍ഷിപ്പ് സിനാരിയോ; ഇന്ത്യന്‍ സാധ്യകള്‍ ഇങ്ങനെ India vs sri lanka",
    "sport": "football",
    "playlistId": "kbfc-isl",
    "playlistTitle": "Kerala Blasters & Indian Football",
    "published": "1mo ago",
    "views": "5K views",
    "summary": "ലോക ടെസ്റ്റ് ചാമ്പ്യന്‍ഷിപ്പ് സിനാരിയോ; ഇന്ത്യന്‍ സാധ്യകള്‍ ഇങ്ങനെ India vs sri lanka"
  },
  {
    "id": "3abRkue6iaw",
    "title": "എൻസോയെ റാഞ്ചാൻ സിറ്റി ! | Real madrid  | Rodri | Barcelona | Enzo Fernandez | Haris Nenmara",
    "sport": "football",
    "playlistId": "PLGWXiMbN17ik",
    "playlistTitle": "Barcelona",
    "published": "1mo ago",
    "views": "16K views",
    "summary": "എൻസോയെ റാഞ്ചാൻ സിറ്റി ! | Real madrid  | Rodri | Barcelona | Enzo Fernandez | Haris Nenmara"
  },
  {
    "id": "RD19bIH3Ppc",
    "title": "നെയ്മറിനെ മയാമി തൂക്കുമോ? ഓര്‍മകളിലെ MSN ട്രയോ.. | MSN | Barcelona | Haris Nenmara",
    "sport": "football",
    "playlistId": "PLGWXiMbN17ik",
    "playlistTitle": "Barcelona",
    "published": "1mo ago",
    "views": "20K views",
    "summary": "നെയ്മറിനെ മയാമി തൂക്കുമോ? ഓര്‍മകളിലെ MSN ട്രയോ.. | MSN | Barcelona | Haris Nenmara"
  },
  {
    "id": "zAQU57tZYho",
    "title": "റോഡ്രിക്കായി പിടിവലി , Rodri | Barcelona | Real Madrid",
    "sport": "football",
    "playlistId": "PLGWXiMbN17ik",
    "playlistTitle": "Barcelona",
    "published": "1mo ago",
    "views": "7.3K views",
    "summary": "റോഡ്രിക്കായി പിടിവലി , Rodri | Barcelona | Real Madrid"
  },
  {
    "id": "JuqZ_w2a5iI",
    "title": "15 കിലോ കുറച്ചു ! സർഫറാസ് വരുന്നു , ഗംഭീർ വെട്ടുമോ?| sarfaraz khan | Haris Nenmara",
    "sport": "cricket",
    "playlistId": "PLcWlSk4Ir_yg",
    "playlistTitle": "Cricket India",
    "published": "2mo ago",
    "views": "10K views",
    "summary": "15 കിലോ കുറച്ചു ! സർഫറാസ് വരുന്നു , ഗംഭീർ വെട്ടുമോ?| sarfaraz khan | Haris Nenmara"
  }
]
};

if (typeof module !== 'undefined' && module.exports) {
  module.exports = FINAL_THIRD_CONFIG;
}
