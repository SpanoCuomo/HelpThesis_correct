import asyncio
import random
import time

from telethon import TelegramClient, events, sync
from telethon.errors import FloodWaitError, UserPrivacyRestrictedError, UserNotMutualContactError
from telethon.tl.functions.channels import GetParticipantsRequest, InviteToChannelRequest
from telethon.tl.types import ChannelParticipantsSearch

# ==================================================================
# CONFIGURAZIONE TELETHON
# ==================================================================

api_id_Luca = 24109055
api_hash_Luca = '1671c82ff0b2a1d8d9aa20e8ae8eb18f'
phone_Luca = '+393349855526'



api_id = api_id_Luca
api_hash = api_hash_Luca
phone = phone_Luca




# Nome sessione (file .session creato localmente)
client = TelegramClient('session_name', api_id, api_hash)

# ==================================================================
# VARIABILI
# ==================================================================

# Se = 1, scarica la lista membri dal gruppo sorgente; 
# se = 0, salta quella parte (per riutilizzare una lista già salvata, ecc.)
fromstart = 1  

# Gruppo sorgente (quello da cui prendere i membri)
source_group_username = 'https://t.me/Concorso_Abilitazione_2023Scuola'

# Gruppo di destinazione (dove invitare)
# ATTENZIONE: deve essere un link valido tipo https://t.me/Qualcosa
destination_group_username = 'https://t.me/+mL7jvfPS6EA1MDNk'

# ==================================================================
# FUNZIONI ASINCRONE
# ==================================================================

async def get_all_participants(client, channel):
    """
    Estrae tutti i partecipanti da un gruppo/ canale usando offset/limit.
    """
    all_participants = []
    offset = 0
    limit = 200

    while True:
        participants = await client(GetParticipantsRequest(
            channel=channel,
            filter=ChannelParticipantsSearch(''),
            offset=offset,
            limit=limit,
            hash=0
        ))
        all_participants.extend(participants.users)
        if len(participants.users) < limit:
            break
        offset += len(participants.users)

    return all_participants

async def invite_members(client, members, destination_group_entity):
    """
    Invita un certo numero di membri (es. 5, 20, ecc.) al gruppo di destinazione.
    Inserisce pause random tra un invito e l'altro per ridurre il rischio di ban.
    """
    numero_da_invitare = 15
    if len(members) < numero_da_invitare:
        numero_da_invitare = len(members)

    # Seleziona casualmente 5 utenti dal totale
    members_to_invite = random.sample(members, numero_da_invitare)

    for user in members_to_invite:
        try:
            # Salta bot o utenti senza ID
            if user.bot or user.id is None:
                continue

            # Invita l'utente
            await client(InviteToChannelRequest(
                channel=destination_group_entity,
                users=[user.id]
            ))

            print(f"Invitato {user.username or user.id}")

            # Pausa casuale tra 60 e 200 secondi
            tempo_attesa = random.uniform(60, 200)
            print(f"Aspetto {tempo_attesa:.1f} secondi prima del prossimo invito...")
            await asyncio.sleep(tempo_attesa)

        except FloodWaitError as e:
            print(f"[FloodWaitError] Devo aspettare {e.seconds} secondi...")
            time.sleep(e.seconds)  # Qui usiamo time.sleep (bloccante) o meglio await asyncio.sleep(e.seconds)
        except (UserPrivacyRestrictedError, UserNotMutualContactError):
            print(f"Impossibile invitare {user.username or user.id} a causa delle sue impostazioni di privacy.")
        except Exception as ex:
            print(f"Errore generico invitando {user.username or user.id}: {ex}")

async def main():
    """
    Funzione principale asincrona. 
    1) Avvia il client. 
    2) Scarica la lista dal gruppo sorgente (se fromstart=1). 
    3) Invita alcuni membri al gruppo di destinazione.
    """
    print("Avvio client e login...")
    await client.start(phone=phone)
    print("Login effettuato correttamente.")

    # Se devi scaricare i membri dal gruppo sorgente
    if fromstart == 1:
        print(f"Recupero lista membri da: {source_group_username}")
        source_group = await client.get_entity(source_group_username)
        members = await get_all_participants(client, source_group)
        print("Totale membri trovati:", len(members))
    else:
        # Se non devi recuperarli da zero, potresti caricarli da un file .json o .csv
        # qui come esempio, mettiamo members vuoto
        members = []
        print("Salto il recupero membri (fromstart=0), members è vuoto o da definire.")

    # Ora ottieni l'entità del tuo gruppo di destinazione
    print(f"Ottengo entità del gruppo di destinazione: {destination_group_username}")
    destination_group_entity = await client.get_entity(destination_group_username)

    # Invita i membri
    if members:
        await invite_members(client, members, destination_group_entity)
    else:
        print("Nessun membro da invitare.")

# ==================================================================
# ESECUZIONE
# ==================================================================
if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(main())
