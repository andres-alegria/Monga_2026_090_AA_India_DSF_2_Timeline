// Editorial text for the timeline: the one source for both the web version (app.js) and the static graphic
// (../output/fig1_build.py). Keep the object after the = sign valid JSON: no comments or trailing commas inside it.
//
// Every title, subhead and body is verbatim from "Deep sea fisheries policy changes timeline_v2.docx" (6 Oct 2026).
// An empty subhead ("") means the entry has none.
// **double asterisks** mark the phrases the reporter set in bold; the web version highlights them.
// start / end: first and last year of the period, inclusive. "ongoing": true draws the bar to the end of the axis.
// icon: a Phosphor icon name from assets/icons.js.
window.DSF_TIMELINE = {
  "title": "India’s deep-sea fishing policy: 1950s to present",
  "deck": "From mechanisation and foreign vessels to indigenous fleets and high-seas fishing, India’s deep-sea ambitions have repeatedly changed course.",
  "axis": {
    "start": 1950,
    "end": 2027,
    "ticks": [
      1950,
      1960,
      1970,
      1980,
      1990,
      2000,
      2010,
      2020
    ]
  },
  "events": [
    {
      "date": "1950s–60s",
      "start": 1950,
      "end": 1969,
      "icon": "engine",
      "title": "Mechanisation begins",
      "subhead": "India looks beyond traditional fishing",
      "body": "The government promotes **mechanisation of indigenous fishing vessels** and exploratory fishing to increase catches and exports. The Indo-Norwegian Project and FAO support the introduction of new vessel designs, including small mechanised boats and larger specialised vessels. Penaid prawn is recognised as an important item for export. Over time, the approach shifts towards **more intensive, export-oriented fishing**, including bottom trawling and onboard freezing."
    },
    {
      "date": "1969–1974",
      "start": 1969,
      "end": 1974,
      "icon": "handshake",
      "title": "Enter foreign partnerships",
      "subhead": "Indian firms are encouraged to bring in foreign vessels",
      "body": "Fishing is designated a priority area for **foreign collaboration**. Indian companies are encouraged to lease or import foreign fishing vessels to expand production and participate in the export trade. Deep Sea Fishing Station is renamed Exploratory Fisheries Project in 1974."
    },
    {
      "date": "1975–79",
      "start": 1975,
      "end": 1979,
      "icon": "flag",
      "title": "Foreign vessels enter India’s EEZ",
      "subhead": "Technology transfer becomes a policy objective",
      "body": "After India establishes its **200-nautical-mile Exclusive Economic Zone (EEZ)** in 1976, foreign-flagged vessels are allowed to fish in Indian waters through licences and partnerships. The first deep-sea policy in 1977 provided for chartering arrangements with foreign operators. Private entrepreneurs are permitted to import trawlers."
    },
    {
      "date": "1980–1985",
      "start": 1980,
      "end": 1985,
      "icon": "gavel",
      "title": "Regularising foreign fishing vessels in Indian waters",
      "subhead": "",
      "body": "Maritime Zones of India (Regulation of Fishing by Foreign Vessels) Act, 1981 regulates foreign vessels operating in Indian waters. Exploratory Fisheries Project is renamed the Fishery Survey of India (1983). Joint ventures are promoted to bring in **technology, resource surveys and fishing expertise**, while helping Indian enterprises enter the export market."
    },
    {
      "date": "1985–96",
      "start": 1985,
      "end": 1996,
      "icon": "fish",
      "title": "From shrimp to tuna",
      "subhead": "India turns towards offshore resources",
      "body": "As shrimp fisheries become increasingly unsustainable, policy attention shifts towards **tuna and tuna-like species** that occur farther offshore. Between 1985 and 1996, **189 Taiwanese longliners** enter Indian waters through charter, lease and joint-venture arrangements, becoming a major part of the country’s deep-sea fishing effort."
    },
    {
      "date": "1991",
      "start": 1991,
      "end": 1991,
      "icon": "scroll",
      "title": "Deep Sea Fishing Policy opens the sector",
      "subhead": "Foreign vessels, test fishing and joint ventures",
      "body": "As part of wider economic reforms, India introduces a new **Deep Sea Fishing Policy**. It allows foreign vessels to operate through leasing arrangements, permits foreign test fishing and promotes **49:51 foreign-Indian joint ventures** covering fishing, processing and marketing. Around **400 vessels receive valid permits** under the policy."
    },
    {
      "date": "1992–97",
      "start": 1992,
      "end": 1997,
      "icon": "megaphone",
      "title": "Fisher protests force a rethink",
      "subhead": "Foreign vessels face growing opposition",
      "body": "Millions of fishers and fish workers mobilise against the policy, arguing that foreign and larger vessels could cause **encroachment on fishing grounds, over-exploitation and damage to fishing gear and craft**. Following sustained protests and recommendations of the **P. Murari Committee Report**, the 1991 Deep Sea Fishing Policy is rescinded. Foreign fishing under these schemes ends."
    },
    {
      "date": "1997–2002",
      "start": 1997,
      "end": 2002,
      "icon": "file-dashed",
      "title": "Policy vacuum",
      "subhead": "",
      "body": "By the end of 2003, the sector had evolved without a settled deep-sea policy."
    },
    {
      "date": "2004",
      "start": 2004,
      "end": 2004,
      "icon": "boat",
      "title": "India turns towards a domestic fleet",
      "subhead": "Resource-specific vessels replace broad foreign collaboration",
      "body": "The Comprehensive Policy on Marine Fisheries promotes **Indian-owned, resource-specific vessels** for deep-sea species such as tuna and squid. It also provides incentives for wholly Indian-owned vessels to venture into **international waters** and pursue fishing arrangements with other nations."
    },
    {
      "date": "2014–17",
      "start": 2014,
      "end": 2017,
      "icon": "clipboard-text",
      "title": "A bigger deep-sea fleet is proposed",
      "subhead": "But the proposal meets resistance",
      "body": "The Meenakumari Committee argues that India’s deep-sea fleet remains under-equipped and recommends **270 additional vessels**, including tuna longliners and squid jiggers. It also proposes foreign technology transfer to build domestic capacity. The recommendations trigger strong opposition from fishers and coastal governments. In **2017, the government revokes access agreements** for foreign fishing vessels in the Indian EEZ."
    },
    {
      "date": "2017",
      "start": 2017,
      "end": 2017,
      "icon": "users-three",
      "title": "Push for an indigenous deep-sea fleet",
      "subhead": "Fishers and indigenous capacity take centre stage",
      "body": "The National Policy on Marine Fisheries promotes the **modernisation of existing indigenous vessels** and the introduction of new deep-sea fishing vessels. It specifically encourages participation through **fisher cooperatives and self-help groups**, marking a renewed emphasis on domestic capacity."
    },
    {
      "date": "2020",
      "start": 2020,
      "end": 2020,
      "icon": "currency-inr",
      "title": "Deep-sea fishing gets a major funding push",
      "subhead": "Subsidies support traditional fishers",
      "body": "The **₹20,000-crore PM Matsya Sampada Yojana** provides a major push for deep-sea fishing. A significant allocation supports traditional fishers in acquiring **indigenous deep-sea fishing vessels**, including vessels targeting tuna, tuna-like species, billfish and sharks."
    },
    {
      "date": "2025–present",
      "start": 2025,
      "end": 2026,
      "ongoing": true,
      "icon": "globe-hemisphere-east",
      "title": "India looks to the high seas",
      "subhead": "Indian-flagged vessels move beyond the EEZ",
      "body": "India is renewing its focus on **high-seas fishing and high-value species**, particularly tuna and tuna-like species. New guidelines and authorisations provide a framework for Indian-flagged vessels with valid permissions to fish **beyond India’s EEZ**, while recent policy initiatives continue to emphasise domestic deep-sea fishing capacity."
    }
  ],
  "source": "Source: Mongabay reporting.",
  "ui": {
    "navLabel": "Policy shifts, 1950s to present",
    "prev": "Previous",
    "next": "Next",
    "of": "of",
    "fallbackAlt": "Static version of the timeline"
  }
};
