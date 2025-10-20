# Monster Hunter - Quick Reference Guide

## 🎮 Project Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    MONSTER HUNTER GAME                       │
│         Pokemon-style RPG built with Pygame CE 2.5.5         │
└─────────────────────────────────────────────────────────────┘
```

## 📦 Project Structure (8 Core Modules)

```
code/
├── 🎯 main.py           - Game loop & state management
├── ⚙️  settings.py       - Global configurations
├── 📊 game_data.py      - Monsters, Trainers, Attacks data
├── 🎭 entities.py       - Player & NPC characters
├── 🐉 monster.py        - Monster stats & abilities
├── ⚔️  battle.py         - Turn-based combat system
├── 💬 dialog.py         - NPC dialog trees
└── 🖼️  sprites.py        - All sprite classes
```

## 🧩 Computational Thinking Applied

### 1️⃣ DECOMPOSITION (Chia Nhỏ)

```
Monster Hunter Game
│
├── 🌍 Overworld System
│   ├── Map loading (TMX)
│   ├── Player movement
│   ├── NPC interactions
│   └── Random encounters
│
├── ⚔️ Battle System
│   ├── Turn management (initiative)
│   ├── Combat actions (Fight/Defend/Switch/Catch)
│   ├── Damage calculation
│   └── Victory/defeat handling
│
├── 🐉 Monster System
│   ├── Stats management
│   ├── Abilities/Attacks
│   ├── XP & Leveling
│   └── Evolution chains
│
└── 🎨 Presentation Layer
    ├── Sprite rendering
    ├── UI elements
    ├── Animations
    └── Audio
```

### 2️⃣ PATTERN RECOGNITION (Nhận Dạng Mẫu)

#### Mathematical Patterns

| Pattern Type | Formula | Example |
|-------------|---------|---------|
| **XP Scaling** | `level × 150` | Lv10 = 1,500 XP |
| **Stat Scaling** | `base_stat × level` | HP(Lv10) = 15×10 = 150 |
| **Type Effectiveness** | `×2.0, ×1.0, ×0.5` | Fire→Plant = ×2 |
| **Initiative** | `speed × dt` | Speed 2.0 = 2x turns |

#### Design Patterns

```
🎯 State Machine
   Overworld ↔ Battle ↔ Dialog ↔ Evolution

🏭 Factory Pattern
   create_monster() → MonsterSprite + 4 UI components

👁️ Observer Pattern
   Timer(callback) → Event triggers

🧱 Component Pattern
   MonsterSprite = Core + Outline + Name + Level + Stats
```

### 3️⃣ ABSTRACTION (Trừu Tượng)

```
Entity (Abstract Base)
├── Common: position, animation, movement
│
├── Player (Concrete)
│   └── Specific: keyboard input
│
└── Character (Concrete)
    └── Specific: AI behavior, dialog
```

**Key Abstraction**: Giữ lại interface chung, ẩn đi implementation details

### 4️⃣ ALGORITHMIC THINKING (Tư Duy Thuật Toán)

#### Core Algorithms

```python
# 1. Battle Turn System - O(n)
for monster in all_monsters:
    if monster.initiative >= 100:
        execute_turn(monster)
        break

# 2. Damage Calculation - O(1)
damage = attack × type_multiplier × defense_factor
final = max(1, damage)  # Minimum 1 damage

# 3. Collision Detection - O(m)
for sprite in collision_sprites:
    if hitbox.colliderect(sprite.hitbox):
        resolve_collision()

# 4. XP Distribution - O(k)
xp_per_monster = total_xp / num_alive_monsters
for monster in alive_monsters:
    monster.xp += xp_per_monster
    check_level_up()
```

## 📊 Key Statistics

```
┌─────────────────────────────────────────────┐
│              PROJECT METRICS                 │
├─────────────────────────────────────────────┤
│ Total Lines of Code     : ~3,000+           │
│ Number of Modules       : 8                 │
│ Number of Classes       : 30+               │
│ Number of Monsters      : 14                │
│ Number of Attacks       : 11                │
│ Number of Trainers      : 30+               │
│ Target FPS              : 60                │
│ Complexity              : Low-Medium ✅      │
│ Performance             : O(n) per frame ✅  │
└─────────────────────────────────────────────┘
```

## ⚡ Performance Characteristics

| Operation | Time Complexity | Notes |
|-----------|----------------|-------|
| Monster Update | O(n) | n = active monsters |
| Damage Calc | O(1) | Constant time ✅ |
| Collision Check | O(m) | m = collision sprites |
| XP Award | O(k) | k = alive monsters |
| Battle Turn | O(n) | Linear scan |
| **Overall** | **O(n)** | **Excellent** ✅ |

## 🎨 Type Effectiveness Chart

```
        🔥 FIRE
         ╱    ╲
      ×2╱      ╲×0.5
       ╱        ╲
      ╱          ╲
   🌿 PLANT ──×2──→ 💧 WATER
      ╲          ╱
    ×0.5╲      ╱×2
         ╲    ╱
          ╲  ╱
         💧 WATER

Rock-Paper-Scissors circular relationship
```

## 🔄 Game Loop Flow

```
┌─────────────────────────────────────────────┐
│          MAIN GAME LOOP (60 FPS)            │
└─────────────────────────────────────────────┘

  ┌──────────────────┐
  │  Handle Events   │ (Keyboard, quit, etc.)
  └────────┬─────────┘
           │
           ▼
  ┌──────────────────┐
  │   Update Phase   │
  ├──────────────────┤
  │ • Timer updates  │
  │ • Input handling │
  │ • Entity movement│
  │ • Battle logic   │
  │ • Collisions     │
  └────────┬─────────┘
           │
           ▼
  ┌──────────────────┐
  │   Render Phase   │
  ├──────────────────┤
  │ • Sort sprites   │
  │ • Draw world     │
  │ • Draw UI        │
  │ • Transitions    │
  └────────┬─────────┘
           │
           ▼
  ┌──────────────────┐
  │  Display Flip    │ (Show frame to screen)
  └────────┬─────────┘
           │
           └─────────────► (Repeat at 60 FPS)
```

## 🐉 Monster Evolution Chains

```
🌿 PLANT LINE:
Plumette (Lv1) → Ivieron (Lv15) → Pluma (Lv32)
Larvea (Lv1) → Cleaf (Lv4)

🔥 FIRE LINE:
Sparchu (Lv1) → Cindrill (Lv15) → Charmadillo (Lv33)

💧 WATER LINE:
Finsta (Lv1) → Gulfin (Lv34) → Finiette (Lv45)
```

## 🎯 Battle Actions

```
┌─────────────────────────────────────────────┐
│            PLAYER TURN OPTIONS              │
├─────────────────────────────────────────────┤
│                                             │
│  ⚔️  FIGHT    → Choose attack → Choose target │
│  🛡️  DEFEND   → Reduce damage by 20%         │
│  🔄 SWITCH   → Change active monster        │
│  🖐️  CATCH    → Capture wild monster         │
│                 (must be <90% HP)           │
└─────────────────────────────────────────────┘
```

## 📈 Stat Scaling Examples

```
SPARCHU (base_health = 15, base_speed = 1.0)

Level │ Health │ Energy │ Attack │ Speed │ XP Required
──────┼────────┼────────┼────────┼───────┼─────────────
  1   │   15   │    7   │   3.0  │  1.0  │     150
  5   │   75   │   35   │  15.0  │  5.0  │     750
 10   │  150   │   70   │  30.0  │ 10.0  │   1,500
 15   │  225   │  105   │  45.0  │ 15.0  │   2,250
 20   │  300   │  140   │  60.0  │ 20.0  │   3,000
 32   │  480   │  224   │  96.0  │ 32.0  │   4,800

Linear scaling: All stats × level
```

## 🎓 Code Quality Scores

```
┌─────────────────────────────────────────────┐
│         COMPUTATIONAL THINKING SCORES        │
├─────────────────────────────────────────────┤
│ Decomposition         : 9/10 ⭐⭐⭐⭐⭐        │
│ Pattern Recognition   : 9/10 ⭐⭐⭐⭐⭐        │
│ Abstraction           : 8.5/10 ⭐⭐⭐⭐⭐      │
│ Algorithmic Thinking  : 9/10 ⭐⭐⭐⭐⭐        │
├─────────────────────────────────────────────┤
│ OVERALL GRADE         : A+ (95/100) 🎉      │
└─────────────────────────────────────────────┘
```

## 🚀 Top 5 Recommendations

### 1. Save/Load System
```python
SaveSystem.save_game(player_monsters, game_state)
SaveSystem.load_game(slot_number)
```
**Impact**: High | **Effort**: Medium

### 2. Enhanced AI
```python
class BattleAI:
    def choose_action(self):
        # Smart decision making
        # - Heal when low HP
        # - Type advantage
        # - Target selection
```
**Impact**: High | **Effort**: Medium

### 3. Particle Effects
```python
ParticleSystem.emit_hit_effect(position, element)
ParticleSystem.emit_damage_numbers(position, damage)
```
**Impact**: Medium | **Effort**: Low

### 4. Status Effects
```python
StatusEffect('burn', duration=3, tick_damage=5)
StatusEffect('paralyze', duration=2)
```
**Impact**: High | **Effort**: High

### 5. More Content
- 20+ new monsters
- 5+ new biomes
- 10+ new attacks
**Impact**: High | **Effort**: High

## 📚 Key Files to Read

```
START HERE:
1. 📖 settings.py      - Understand constants
2. 📖 game_data.py     - See all monsters/attacks
3. 📖 monster.py       - Core monster logic
4. 📖 battle.py        - Battle system
5. 📖 main.py          - Tie everything together
```

## 🎮 Controls

```
┌─────────────────────────────────────────────┐
│              GAME CONTROLS                   │
├─────────────────────────────────────────────┤
│ Movement        : Arrow Keys / WASD          │
│ Interact/Select : SPACE                      │
│ Monster Index   : ENTER                      │
│ Back/Cancel     : ESC                        │
│ Quit Game       : ESC (from main menu)       │
└─────────────────────────────────────────────┘
```

## 💾 Tech Stack

```
┌─────────────────────────────────────────────┐
│            TECHNOLOGY STACK                  │
├─────────────────────────────────────────────┤
│ Language   : Python 3.13.7                   │
│ Framework  : Pygame CE 2.5.5                 │
│ Maps       : PyTMX (Tiled map loader)        │
│ Platform   : Cross-platform                  │
│            : (Windows, macOS, Linux)         │
└─────────────────────────────────────────────┘
```

## 🎯 Learning Goals Achieved

✅ **Game Architecture** - Modular design  
✅ **OOP Principles** - Inheritance, composition  
✅ **Algorithm Design** - Efficient O(n) systems  
✅ **State Management** - Game states & transitions  
✅ **Data-Driven Design** - JSON-like data structures  
✅ **Error Handling** - Try/except with fallbacks  
✅ **Code Documentation** - Docstrings & comments  
✅ **Performance Optimization** - 60 FPS maintained  

---

## 📞 Quick Commands

```bash
# Run the game
python code/main.py

# Check Python version
python --version  # Should be 3.13.7

# Install dependencies (if needed)
pip install pygame-ce pytmx
```

---

**Generated**: Quick Reference Guide  
**Last Updated**: 2025-10-20  
**Version**: 1.0
