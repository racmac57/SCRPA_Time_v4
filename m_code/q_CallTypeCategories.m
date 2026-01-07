// ===========================================
// STAGING QUERY: Call Type Categories
// Purpose: Load and buffer call type mapping CSV
// Disable Load: Yes (referenced by Updated_All_Crimes)
// Optimized: Removed PromoteAllScalars, simplified transformation
// ===========================================
let CallTypeCategoriesRaw = Csv.Document(
        File.Contents("C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Classifications\CallTypes\CallType_Categories.csv"),
        [ Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv ]),
    CallTypeCategories0 = Table.PromoteHeaders(CallTypeCategoriesRaw),
    CallTypeCategories = Table.Buffer(Table.TransformColumnTypes(
        CallTypeCategories0, {{"Incident", type text},
                              {"Incident_Norm", type text},
                              {"Category_Type", type text},
                              {"Response_Type", type text}}))
                             in CallTypeCategories