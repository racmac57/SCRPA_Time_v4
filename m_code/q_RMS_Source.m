// 🕒 2026_01_13_11_11_31
// Project: m_code/q_RMS_Source.m
// Author: R. A. Carucci
// Purpose: Staging query to automatically load the most recent RMS Excel export file from the designated folder for processing

// ===========================================
// STAGING QUERY: RMS Source Data
// Purpose: Load latest Excel file from folder
// Disable Load: Yes (referenced by Updated_All_Crimes)
// ===========================================
let FolderPath = "C:\Users\carucci_r\OneDrive - City of Hackensack\05_EXPORTS\_RMS\scrpa",
    AllFiles = Folder.Files(FolderPath),
    XlsxFiles = Table.SelectRows(
        AllFiles,
        each Text.EndsWith([Name], ".xlsx", Comparer.OrdinalIgnoreCase)),
    SortedFiles = Table.Sort(XlsxFiles, {{"Date modified", Order.Descending}}),
    LatestFilePath = SortedFiles{0}[Folder Path] & SortedFiles{0}[Name],
    Source = Excel.Workbook(File.Contents(LatestFilePath), true),
    FirstTable = Source{0}[Data] in FirstTable