# 🗺️ Rocket Launch Locations

These are **official and historically active launch sites** you can include in your Go/No-Go Advisor app.  
Each includes coordinates, operator details, and basic legal status.

---

## 🇺🇸 United States

### **Kennedy Space Center (LC-39A / LC-39B)**
- **Location:** Merritt Island, Florida, USA  
- **Coordinates:** `28.6084° N, 80.6043° W`  
- **Operator:** NASA  
- **Used by:** SpaceX, NASA (Falcon 9, Falcon Heavy, SLS)  
- **Launch Types:** Orbital, Crew, Cargo  
- **Legal status:** ✔️ **Fully licensed and regulated** under FAA & NASA authority.

---

### **Cape Canaveral Space Force Station (SLC-40 / SLC-41 / SLC-46)**
- **Location:** Cape Canaveral, Florida, USA  
- **Coordinates:** `28.5618° N, 80.5772° W`  
- **Operator:** U.S. Space Force  
- **Used by:** SpaceX, ULA, Astra, others  
- **Launch Types:** Orbital, LEO, GTO  
- **Legal status:** ✔️ FAA-licensed commercial launches permitted.

---

### **Vandenberg Space Force Base**
- **Location:** Lompoc, California, USA  
- **Coordinates:** `34.7420° N, 120.5724° W`  
- **Operator:** U.S. Space Force  
- **Used by:** SpaceX, Rocket Lab, NASA, DoD  
- **Launch Types:** Polar / Sun-synchronous orbits  
- **Legal status:** ✔️ Approved and heavily regulated; good for polar trajectories.

---

### **Wallops Flight Facility**
- **Location:** Wallops Island, Virginia, USA  
- **Coordinates:** `37.9400° N, 75.4660° W`  
- **Operator:** NASA  
- **Used by:** Northrop Grumman (Antares, Minotaur), smallsat missions  
- **Launch Types:** Suborbital and orbital  
- **Legal status:** ✔️ Licensed under FAA; primarily for smaller payloads.

---

### **Pacific Spaceport Complex — Alaska (PSCA)**
- **Location:** Kodiak Island, Alaska, USA  
- **Coordinates:** `57.4352° N, 152.3394° W`  
- **Operator:** Alaska Aerospace Corporation  
- **Used by:** Astra, Rocket Lab (future), military  
- **Launch Types:** Polar, suborbital  
- **Legal status:** ✔️ FAA-licensed.

---

### **Kwajalein Atoll (Reagan Test Site)**
- **Location:** Marshall Islands (U.S. military territory)  
- **Coordinates:** `9.3960° N, 167.4700° E`  
- **Operator:** U.S. Army / SpaceX (historical)  
- **Used by:** Early SpaceX Falcon 1 launches  
- **Launch Types:** Orbital  
- **Legal status:** ✔️ Military-controlled, special access required.

---

## 🌍 International Sites

### **Guiana Space Centre (Centre Spatial Guyanais)**
- **Location:** Kourou, French Guiana (France)  
- **Coordinates:** `5.2360° N, 52.7750° W`  
- **Operator:** CNES / Arianespace / ESA  
- **Used by:** Ariane, Vega, Soyuz (ESA)  
- **Launch Types:** Equatorial, orbital  
- **Legal status:** ✔️ Internationally recognized spaceport; permission via CNES/ESA.

---

### **Baikonur Cosmodrome**
- **Location:** Baikonur, Kazakhstan  
- **Coordinates:** `45.9200° N, 63.3420° E`  
- **Operator:** Roscosmos (Russia, leased from Kazakhstan)  
- **Used by:** Soyuz, Progress, crewed and cargo missions  
- **Launch Types:** Orbital  
- **Legal status:** ⚠️ Access restricted; foreign launches require diplomatic agreements.

---

### **Tanegashima Space Center**
- **Location:** Tanegashima Island, Japan  
- **Coordinates:** `30.4017° N, 130.9740° E`  
- **Operator:** JAXA  
- **Used by:** H-IIA, H3 launch vehicles  
- **Launch Types:** Orbital (LEO, GTO)  
- **Legal status:** ✔️ Licensed by JAXA; permission required for external partners.

---

### **Satish Dhawan Space Centre (Sriharikota)**
- **Location:** Andhra Pradesh, India  
- **Coordinates:** `13.7331° N, 80.2350° E`  
- **Operator:** ISRO  
- **Used by:** PSLV, GSLV  
- **Launch Types:** Orbital  
- **Legal status:** ✔️ Operated by ISRO; requires ISRO approval for collaborations.

---

### **Rocket Lab Launch Complex 1**
- **Location:** Māhia Peninsula, New Zealand  
- **Coordinates:** `-39.2628° S, 177.8644° E`  
- **Operator:** Rocket Lab  
- **Used by:** Electron, Neutron (future)  
- **Launch Types:** LEO, Sun-synchronous  
- **Legal status:** ✔️ Licensed under New Zealand’s Space Agency.

---

### **Spaceport Cornwall**
- **Location:** Newquay, United Kingdom  
- **Coordinates:** `50.4400° N, 5.0100° W`  
- **Operator:** UK Space Agency / Virgin Orbit (formerly)  
- **Used by:** Horizontal launches (air-launched rockets)  
- **Launch Types:** Air-launched smallsats  
- **Legal status:** ✔️ Licensed under the UK Space Industry Act (2018).

---

## ⚠️ Legal Summary

| Symbol | Meaning |
|--------|----------|
| ✔️ | Legally approved and currently operational for licensed launches |
| ⚠️ | Restricted or requires diplomatic / special clearance |
| ❌ | Closed or unapproved for orbital launches |

---

## ✅ Recommended “Legal & Practical” Options for Your App

For simplicity and realism, your **Go/No-Go Advisor app** should include the following selectable launch sites:

| Code | Name | Country |
|------|------|----------|
| `KSC_LC39A` | Kennedy Space Center (LC-39A) | USA |
| `CCSFS_SLC40` | Cape Canaveral Space Force Station | USA |
| `VAFB` | Vandenberg Space Force Base | USA |
| `WFF` | Wallops Flight Facility | USA |
| `PSCA` | Pacific Spaceport Complex (Alaska) | USA |
| `GSC` | Guiana Space Centre | France (ESA) |
| `TSC` | Tanegashima Space Center | Japan |
| `SDSC` | Satish Dhawan Space Centre | India |
| `RL_Mahia` | Rocket Lab Launch Complex 1 | New Zealand |
| `SPC_UK` | Spaceport Cornwall | United Kingdom |
