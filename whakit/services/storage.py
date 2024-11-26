# # whakit/services/storage_service.py

# import asyncio
# import logging

# from google.oauth2.service_account import Credentials
# from googleapiclient.discovery import build

# logger = logging.getLogger(__name__)


# class StorageService:
#     def __init__(self):
#         credentials = Credentials.from_service_account_file(
#             "whakit/credentials/credentials.json",
#             scopes=["https://www.googleapis.com/auth/spreadsheets"],
#         )
#         self.service = build("sheets", "v4", credentials=credentials)

#     async def append_to_sheet(self, spreadsheet_id: str, data: list):
#         sheet = self.service.spreadsheets()
#         request = sheet.values().append(
#             spreadsheetId=spreadsheet_id,
#             range="Sheet1",
#             valueInputOption="RAW",
#             insertDataOption="INSERT_ROWS",
#             body={"values": [data]},
#         )
#         try:
#             await asyncio.get_event_loop().run_in_executor(None, request.execute)
#             logger.info("Data appended to Google Sheets successfully.")
#         except Exception as e:
#             logger.error(f"Error appending to Google Sheets: {e}")
