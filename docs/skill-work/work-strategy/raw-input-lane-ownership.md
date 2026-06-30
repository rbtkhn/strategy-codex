# Raw-Input Lane Ownership


This note gives the ownership rule for raw-input captures when a host channel and a recurring expert lane point in different directions.

## Core rule

- use **host-first ownership** when the upload belongs to a **designated cognition stream**
- use **expert-first ownership** when the upload lives on an **outside channel** and the recurring guest already has the real notebook lane

## Host-first

Use **host-first** when the upload belongs to a designated stream such as:

- Diesen
- Davis
- Mercouris
- Dialogue Works

Examples:

- `Diesen x Freeman` raw-input belongs to the **Diesen** stream
- `Davis x Barnes` raw-input belongs to the **Davis** stream

In those cases, the filename should begin with the host stream and `thread:` should follow the host stream. The guest still stays visible in `guest:`, title, and later routing objects.

## Expert-first

Use **expert-first** when the host channel is not itself a designated cognition stream and the guest already has a stable expert lane.

Examples:

- `Mario Nawfal x Pape` raw-input should be **Pape-first**
- outside-channel `Ritter` interviews should usually be **Ritter-first**

In those cases, the filename should begin with the expert lane and `thread:` should follow the expert lane. The outside host still remains visible in `show`, `host`, `channel_slug`, and title context.

## Do not duplicate by default

Do not create both a host-owned and expert-owned raw-input file by default just because both sides are notable.

Only create a second ownership surface when the operator explicitly wants it.

## Short test

Ask:

- is this upload itself part of a designated cognition stream? -> **host-first**
- or is the host only an outside container while the guest is the real recurring notebook owner? -> **expert-first**

If you need the boundary between this ingest rule and later `speaker arc` logic, read [raw-input-ownership-vs-speaker-arc.md](raw-input-ownership-vs-speaker-arc.md).
