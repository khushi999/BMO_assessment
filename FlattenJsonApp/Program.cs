using System;
using System.IO;
using System.Collections.Generic;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

class FlattenJson
{
    static void Main(string[] args)
    {
        // Define input JSON file and output CSV file paths
        string jsonPath = "sample_data.json";
        string outputPath = "flattened_lctr_data_q4.csv";

        // Exit if JSON file doesn't exist
        if (!File.Exists(jsonPath))
        {
            Console.WriteLine("JSON file not found.");
            return;
        }

        // Read and parse the JSON file into a JObject
        var jsonText = File.ReadAllText(jsonPath);
        var jsonObj = JsonConvert.DeserializeObject<JObject>(jsonText);

        var flatList = new List<Dictionary<string, string>>();

        // Extract transactions array and flatten each transaction
        if (jsonObj["transactions"] is JArray transactions)
        {
            foreach (JObject item in transactions)
            {
                var flatDict = new Dictionary<string, string>();
                Flatten(item, flatDict);   // Recursive flattening
                flatList.Add(flatDict);
            }
        }

        // Write to CSV
        if (flatList.Count > 0)
        {
            using (var writer = new StreamWriter(outputPath))
            {
                // Write headers using dictionary keys
                var headers = string.Join(",", flatList[0].Keys);
                writer.WriteLine(headers);

                // Write each row of flattened values
                foreach (var row in flatList)
                {
                    var line = string.Join(",", row.Values);
                    writer.WriteLine(line);
                }
            }

            Console.WriteLine($"Flattened data saved to: {outputPath}");
        }
        else
        {
            Console.WriteLine("No data to flatten.");
        }
    }

    // Recursive flatten function to handle nested objects, arrays, and values
    static void Flatten(JToken token, Dictionary<string, string> flatDict, string prefix = "")
    {
        if (token is JObject obj)
        {
            foreach (var prop in obj.Properties())
            {
                Flatten(prop.Value, flatDict, $"{prefix}{prop.Name}.");
            }
        }
        else if (token is JValue val)
        {
            flatDict[prefix.TrimEnd('.')] = val.ToString();   // Save value with key
        }
        else if (token is JArray arr)
        {
            int index = 0;
            foreach (var item in arr)
            {
                Flatten(item, flatDict, $"{prefix}{index}.");  // Append index for arrays
                index++;
            }
        }
    }
}
