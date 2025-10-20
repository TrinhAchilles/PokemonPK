# Monster Hunter - Biểu Đồ Kiến Trúc

## 1. Game State Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        GAME STATES                           │
└─────────────────────────────────────────────────────────────┘

                    ┌──────────────┐
                    │  GAME START  │
                    └──────┬───────┘
                           │
                           ▼
                  ┌────────────────┐
                  │   OVERWORLD    │◄────────────────┐
                  │  (Exploration) │                 │
                  └────┬───────┬───┘                 │
                       │       │                     │
        ┌──────────────┘       └──────────┐         │
        │                                  │         │
        ▼                                  ▼         │
   ┌─────────┐                      ┌──────────┐    │
   │ DIALOG  │                      │  BATTLE  │────┘
   │  TREE   │                      │  SYSTEM  │
   └────┬────┘                      └─────┬────┘
        │                                 │
        │                                 ▼
        │                          ┌────────────┐
        │                          │ EVOLUTION  │
        │                          │ ANIMATION  │
        │                          └─────┬──────┘
        │                                │
        └────────────────┬───────────────┘
                         │
                         ▼
                  ┌──────────────┐
                  │ MONSTER INDEX│
                  │   (Menu)     │
                  └──────────────┘

Legend:
→ : State transition
◄ : Return to previous state
```

## 2. Battle System Flow

```
┌───────────────────────────────────────────────────────────────┐
│                    BATTLE TURN SYSTEM                          │
└───────────────────────────────────────────────────────────────┘

START BATTLE
     │
     ▼
┌─────────────────────────────────────┐
│  Spawn Monsters (3 vs 3)            │
│  - Player: positions 0,1,2          │
│  - Opponent: positions 0,1,2        │
└──────────────┬──────────────────────┘
               │
               ▼
        ┌──────────────┐
        │ UPDATE LOOP  │ ◄──────────────┐
        └──────┬───────┘                │
               │                        │
               ▼                        │
┌──────────────────────────────┐       │
│ Update All Monster Initiative│       │
│  initiative += speed × dt     │       │
└──────────┬───────────────────┘       │
           │                            │
           ▼                            │
      ┌─────────┐                       │
      │initiative│  NO                  │
      │>= 100?  ├──────────────────────┤
      └────┬────┘                       │
           │ YES                        │
           ▼                            │
    ┌────────────┐                      │
    │Pause All   │                      │
    │Monsters    │                      │
    └─────┬──────┘                      │
          │                             │
          ▼                             │
    ┌──────────┐                        │
    │ Player   │  NO                    │
    │Monster?  ├──────┐                 │
    └────┬─────┘      │                 │
         │ YES        ▼                 │
         │      ┌───────────┐           │
         │      │AI TURN    │           │
         │      │ - Wait 600ms          │
         │      │ - Random ability      │
         │      │ - Choose target       │
         │      │ - Execute attack      │
         │      └─────┬─────┘           │
         │            │                 │
         ▼            │                 │
  ┌──────────────────┴──────┐          │
  │    PLAYER INPUT         │          │
  │  ┌──────┬──────┬──────┐ │          │
  │  │Fight │Defend│Switch│ │          │
  │  │      │      │Catch │ │          │
  │  └───┬──┴──┬───┴──┬───┘ │          │
  └──────┼─────┼──────┼─────┘          │
         │     │      │                │
         ▼     ▼      ▼                │
  ┌──────────────────────────┐         │
  │   Select Attack/Target   │         │
  └───────────┬──────────────┘         │
              │                        │
              ▼                        │
     ┌────────────────┐                │
     │ Execute Action │                │
     │ - Animation    │                │
     │ - Damage calc  │                │
     │ - Apply effect │                │
     └────────┬───────┘                │
              │                        │
              ▼                        │
        ┌──────────┐                   │
        │Resume All│                   │
        │Monsters  │                   │
        └─────┬────┘                   │
              │                        │
              ▼                        │
        ┌──────────┐                   │
        │Check     │  Continue         │
        │Death?    ├───────────────────┘
        └────┬─────┘
             │ Death detected
             ▼
      ┌─────────────┐
      │Spawn        │
      │Replacement? │
      └──────┬──────┘
             │
             ▼
       ┌──────────┐
       │Award XP  │
       └────┬─────┘
            │
            ▼
      ┌───────────┐
      │Battle End?│  NO ──┐
      └────┬──────┘       │
           │ YES          │
           ▼              │
       END BATTLE ◄───────┘
```

## 3. Damage Calculation Flow

```
┌────────────────────────────────────────────────────────────┐
│              DAMAGE CALCULATION PIPELINE                    │
└────────────────────────────────────────────────────────────┘

     INPUT: attacker, defender, attack_name
           │
           ▼
  ┌────────────────────┐
  │ Base Damage        │
  │ = attack_stat ×    │
  │   attack_amount    │
  └─────────┬──────────┘
            │
            ▼
  ┌──────────────────────────┐
  │ Type Effectiveness Check │
  └─────────┬────────────────┘
            │
      ┌─────┴─────┐
      │           │
      ▼           ▼
 ┌─────────┐  ┌──────────┐
 │Super    │  │Not Very  │
 │Effective│  │Effective │
 │× 2.0    │  │× 0.5     │
 └────┬────┘  └────┬─────┘
      │            │
      └─────┬──────┘
            │
            ▼
  ┌────────────────────┐
  │ Defense Reduction  │
  │ factor = 1 -       │
  │  defense/2000      │
  └─────────┬──────────┘
            │
            ▼
      ┌──────────┐
      │Defending?│
      └────┬─────┘
           │
    ┌──────┴──────┐
    │YES          │NO
    ▼             │
┌─────────┐       │
│factor   │       │
│-= 0.2   │       │
└────┬────┘       │
     │            │
     └─────┬──────┘
           │
           ▼
  ┌────────────────┐
  │ Clamp(0.0, 1.0)│
  └────────┬───────┘
           │
           ▼
  ┌────────────────────┐
  │ final_damage =     │
  │  damage × defense  │
  └─────────┬──────────┘
            │
            ▼
      ┌──────────┐
      │Damage > 0│
      │(not heal)│
      └────┬─────┘
           │
    ┌──────┴──────┐
    │YES          │NO
    ▼             │
┌─────────┐       │
│MAX(1.0, │       │
│damage)  │       │
└────┬────┘       │
     │            │
     └─────┬──────┘
           │
           ▼
    ┌──────────────┐
    │Apply to      │
    │monster.health│
    └──────────────┘
           │
           ▼
        OUTPUT
```

## 4. Monster Stats Scaling

```
┌────────────────────────────────────────────────────────────┐
│                MONSTER SCALING FORMULAS                     │
└────────────────────────────────────────────────────────────┘

LEVEL UP XP REQUIREMENT (Linear Growth):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
XP = Level × 150

Level 1:    150 XP   ████
Level 5:    750 XP   ████████████████████
Level 10:  1500 XP   ████████████████████████████████████████
Level 20:  3000 XP   ████████████████████████████████████████████████████████████████████████████████
Level 32:  4800 XP   ███████████████████████████████████████████████████████████████████████████████████████████████████████████████


ACTUAL STATS (Linear Scaling with Level):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Stat = Base_Stat × Level

Example: Sparchu (base_health = 15)
Level 1:   15 HP  ████
Level 5:   75 HP  ████████████████████
Level 10: 150 HP  ████████████████████████████████████████
Level 15: 225 HP  ████████████████████████████████████████████████████████████
Level 32: 480 HP  ████████████████████████████████████████████████████████████████████████████████████████████████████████████


INITIATIVE ACCUMULATION (Speed-based):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Initiative += Speed_Stat × Delta_Time

Finsta (speed=1.8):  ████████████████████████████████  Turn every 55s
Jacana (speed=2.6):  ████████████████████████████████████████████  Turn every 38s  (42% faster!)
Larvea (speed=1.0):  ████████████████  Turn every 100s

Ratio: 1.0 : 1.8 : 2.6
Turns: 1x  : 1.8x: 2.6x  (monsters with higher speed get proportionally more turns)


TYPE EFFECTIVENESS MULTIPLIER:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                      ┌─────────┐
                      │  FIRE   │
                      │  (×2)   │
                      │    ↓    │
    ┌─────────┐       │  PLANT  │       ┌─────────┐
    │  WATER  │───────┤  (×2)   │───────┤  FIRE   │
    │         │  (×2) │    ↓    │ (×2)  │         │
    └─────────┘       │  WATER  │       └─────────┘
                      └─────────┘

Super Effective: ×2.0 damage
Normal:          ×1.0 damage
Not Effective:   ×0.5 damage

Rock Paper Scissors circular relationship!
```

## 5. Entity Class Hierarchy

```
┌────────────────────────────────────────────────────────────┐
│                  ENTITY CLASS DIAGRAM                       │
└────────────────────────────────────────────────────────────┘

                  ┌──────────────────┐
                  │   pygame.sprite  │
                  │     .Sprite      │
                  └────────┬─────────┘
                           │
                           │ inherits
                           ▼
                  ┌──────────────────┐
                  │      Entity      │
                  │  (Abstract Base) │
                  ├──────────────────┤
                  │ + position       │
                  │ + frames         │
                  │ + direction      │
                  │ + speed          │
                  │ + facing_dir     │
                  ├──────────────────┤
                  │ + animate()      │
                  │ + get_state()    │
                  │ + block()        │
                  │ + unblock()      │
                  └────────┬─────────┘
                           │
              ┌────────────┴────────────┐
              │                         │
              ▼                         ▼
     ┌────────────────┐        ┌────────────────┐
     │    Player      │        │   Character    │
     │                │        │    (NPC)       │
     ├────────────────┤        ├────────────────┤
     │+ noticed       │        │+ monsters      │
     │+ collision_spr │        │+ dialog_data   │
     │                │        │+ can_rotate    │
     │                │        │+ has_noticed   │
     ├────────────────┤        │+ radius        │
     │+ input()       │        │+ nurse         │
     │+ move()        │        ├────────────────┤
     │+ collisions()  │        │+ raycast()     │
     └────────────────┘        │+ has_los()     │
                               │+ get_dialog()  │
                               │+ start_move()  │
                               └────────────────┘

RESPONSIBILITIES:
━━━━━━━━━━━━━━━━
Entity:
  - Graphics (animation, frames)
  - Physics (position, velocity)
  - State (facing direction, blocking)

Player:
  - Keyboard input (WASD + Arrows)
  - Collision resolution
  - Camera center point

Character:
  - Dialog interaction
  - Battle initiation
  - Line-of-sight detection
  - AI movement toward player
  - Nurse healing function
```

## 6. Battle Sprite Component System

```
┌────────────────────────────────────────────────────────────┐
│           BATTLE SPRITE COMPOSITION PATTERN                 │
└────────────────────────────────────────────────────────────┘

        ONE MONSTER IN BATTLE = 5 SPRITE COMPONENTS

┌─────────────────────────────────────────────────────────────┐
│                    MonsterSprite (Core)                     │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ - Monster data reference                             │   │
│  │ - Animation frames (idle/attack)                     │   │
│  │ - Attack execution logic                             │   │
│  │ - Timers (highlight, death)                          │   │
│  └──────────────────────────────────────────────────────┘   │
│                          │                                  │
│       ┌──────────────────┼──────────────────┐              │
│       │                  │                  │              │
│       ▼                  ▼                  ▼              │
│  ┌─────────┐      ┌─────────────┐   ┌──────────────┐     │
│  │Outline  │      │NameSprite   │   │LevelSprite   │     │
│  │Sprite   │      │ - Name label│   │ - Level num  │     │
│  │ - White │      │ - BG box    │   │ - XP bar     │     │
│  │  effect │      └─────────────┘   └──────────────┘     │
│  └─────────┘                                               │
│       │                                                    │
│       ▼                                                    │
│  ┌────────────────────────────┐                            │
│  │   MonsterStatsSprite       │                            │
│  │  ┌──────────────────────┐  │                            │
│  │  │ HP bar: ████████░░   │  │                            │
│  │  │ Energy: ██████████   │  │                            │
│  │  │ Initiative: ████░░░░ │  │                            │
│  │  └──────────────────────┘  │                            │
│  └────────────────────────────┘                            │
└─────────────────────────────────────────────────────────────┘

ADVANTAGES OF COMPOSITION:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Single Responsibility Principle
✓ Easy to modify individual components
✓ Independent update/render cycles
✓ Automatic cleanup (when monster dies, all components die)
✓ Reusable components
```

## 7. Data Flow Architecture

```
┌────────────────────────────────────────────────────────────┐
│                   DATA FLOW DIAGRAM                         │
└────────────────────────────────────────────────────────────┘

GAME DATA (Static)
┌──────────────────┐
│ MONSTER_DATA     │ ──┐
│ ATTACK_DATA      │   │
│ TRAINER_DATA     │   │
└──────────────────┘   │
                       │ Read Only
                       ▼
                ┌─────────────┐
                │   Monster   │
                │   Instance  │
                └──────┬──────┘
                       │
         ┌─────────────┼─────────────┐
         │             │             │
         ▼             ▼             ▼
  ┌───────────┐ ┌───────────┐ ┌───────────┐
  │ Battle    │ │ Evolution │ │ Monster   │
  │ System    │ │ System    │ │ Index UI  │
  └─────┬─────┘ └─────┬─────┘ └─────┬─────┘
        │             │             │
        └─────────────┼─────────────┘
                      │
                      ▼
              ┌───────────────┐
              │ Update Stats  │
              │ - Health      │
              │ - Energy      │
              │ - XP/Level    │
              └───────┬───────┘
                      │
                      ▼
              ┌───────────────┐
              │  Persistence  │
              │  (Future)     │
              │  - Save file  │
              │  - Load game  │
              └───────────────┘

INPUT FLOW:
━━━━━━━━━━
Keyboard → Player.input() → direction vector → Entity.move()
           ↓
           Space key → Dialog/Battle interaction
           Return key → Monster Index toggle

RENDER FLOW:
━━━━━━━━━━━
AllSprites.draw() → Sort by Z-layer → Blit to screen
                    Sort by Y-position (for depth)
```

## 8. Module Dependency Graph

```
┌────────────────────────────────────────────────────────────┐
│              MODULE DEPENDENCY GRAPH                        │
└────────────────────────────────────────────────────────────┘

         ┌────────────┐
         │  settings  │ ◄──────────────┐
         │  .py       │                │ Import
         └─────┬──────┘                │
               │                       │
        Import │                       │
               ▼                       │
         ┌────────────┐          ┌─────────┐
         │ game_data  │          │support  │
         │    .py     │          │  .py    │
         └─────┬──────┘          └────┬────┘
               │                      │
               │ Import         Import│
               ▼                      ▼
         ┌────────────┐          ┌──────────┐
         │  monster   │          │ sprites  │
         │    .py     │          │   .py    │
         └─────┬──────┘          └────┬─────┘
               │                      │
               └──────────┬───────────┘
                          │ Import
                          ▼
                    ┌──────────┐
                    │ entities │
                    │   .py    │
                    └────┬─────┘
                         │
              ┌──────────┼──────────┐
              │          │          │
        Import│    Import│    Import│
              ▼          ▼          ▼
         ┌─────────┬─────────┬──────────┐
         │ battle  │ dialog  │evolution │
         │  .py    │  .py    │   .py    │
         └────┬────┴────┬────┴────┬─────┘
              │         │         │
              └─────────┼─────────┘
                   Import│
                        ▼
                  ┌──────────┐
                  │  main    │
                  │   .py    │
                  └──────────┘

DEPENDENCY LEVELS (Bottom to Top):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Level 0: settings.py (no dependencies)
Level 1: game_data.py, support.py (depend on settings)
Level 2: monster.py, sprites.py (depend on Level 1)
Level 3: entities.py (depend on Level 2)
Level 4: battle.py, dialog.py, evolution.py (depend on Level 3)
Level 5: main.py (depends on everything)

COUPLING: LOW ✓ (modules are independent)
COHESION: HIGH ✓ (each module has single purpose)
```

---

## 📊 Performance Characteristics

```
┌────────────────────────────────────────────────────────────┐
│              TIME COMPLEXITY SUMMARY                        │
└────────────────────────────────────────────────────────────┘

Operation                    │ Complexity │ Notes
─────────────────────────────┼────────────┼──────────────────
Monster update (per frame)   │ O(n)       │ n = active monsters
Battle turn check            │ O(n)       │ n = all monsters
Damage calculation           │ O(1)       │ Constant time
Collision detection          │ O(m)       │ m = collision sprites
XP distribution              │ O(k)       │ k = alive monsters
Evolution check              │ O(p)       │ p = player monsters
AI decision making           │ O(n)       │ n = filtering targets
Sprite rendering             │ O(s×log s) │ s = sprites (sorting)

Overall Performance: O(n) per frame - EXCELLENT ✓
Memory Usage: O(n) - LINEAR SCALING ✓
```

---

**Generated**: Computational Thinking Analysis
**Author**: AI Assistant
**Date**: 2025-10-20
