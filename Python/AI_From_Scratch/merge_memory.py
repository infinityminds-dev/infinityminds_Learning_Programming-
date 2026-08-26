import glob
import json


def smart_merge_memories():
    print(
        "================================================================"
    )
    print("      SMART AI MEMORY MERGE ENGINE (Pankaj Master Priority)")
    print(
        "================================================================\n"
    )

    my_file = input(
        "Apni main file ka exact naam daalo (e.g. ai_memory_pankaj_5733.json): "
    ).strip()

    if not my_file:
        print("Error: File ka naam dena zaroori hai!")
        return

    # 1. Apni Master File Load Karo
    try:
        with open(my_file, "r", encoding="utf-8") as f:
            master_data = json.load(f)
    except Exception as e:
        print(
            f"Error: '{my_file}' kholne me problem aayi. Sahi naam check karo! Details: {e}"
        )
        return

    # Master patterns aur responses ka track rakhne ke liye map
    master_map = {}
    for item in master_data:
        tag = item.get("tag", "general")
        for p in item.get("patterns", []):
            p_clean = p.lower().strip()
            responses = item.get("responses", [])
            context_responses = item.get("context_responses", {})
            master_map[p_clean] = {
                "tag": tag,
                "responses": list(responses),
                "context_responses": context_responses,
            }

    # 2. Folder ki baki sabhi files dhundho (Dosto ki files)
    all_files = glob.glob("ai_memory_*.json")
    friend_files = [f for f in all_files if f != my_file]

    if not friend_files:
        print(
            "Folder me merge karne ke liye kisi dost ki nayi memory file nahi mili!"
        )
        return

    print(f"Mili hui dosto ki files: {friend_files}\n")

    added_count = 0

    # 3. Dosto ki files se naya data uthao (Sirf wo jo tumhare paas nahi hai)
    for file_path in friend_files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                friend_data = json.load(f)
                for item in friend_data:
                    for p in item.get("patterns", []):
                        p_clean = p.lower().strip()
                        friend_responses = item.get("responses", [])

                        if p_clean not in master_map:
                            # Agar ye pattern tumhare paas bilkul nahi hai, tabhi add karo
                            master_map[p_clean] = {
                                "tag": item.get(
                                    "tag", f"friend_add_{added_count}"
                                ),
                                "responses": list(friend_responses),
                                "context_responses": item.get(
                                    "context_responses", {}
                                ),
                            }
                            added_count += 1
                        else:
                            # Agar pattern pehle se hai, toh check karo koi naya response toh nahi hai
                            for r in friend_responses:
                                if r not in master_map[p_clean]["responses"]:
                                    master_map[p_clean]["responses"].append(r)
        except Exception as e:
            print(f"File {file_path} read karne me error: {e}")

    # 4. Final Rebuild Master List
    final_master_list = []
    for pat, details in master_map.items():
        final_master_list.append(
            {
                "tag": details["tag"],
                "patterns": [pat],
                "responses": details["responses"],
                "context_responses": details["context_responses"],
            }
        )

    # 5. Tumhari Master File ko update karke save kar do
    with open(my_file, "w", encoding="utf-8") as f:
        json.dump(final_master_list, f, indent=2, ensure_ascii=False)

    print(
        f"\nSUCCESS! Total {added_count} naye patterns dosto ki files se tumhari '{my_file}' me safely merge ho gaye hain!"
    )
    print(
        "Tumhara original brain aur priority data 100% safe hai. Maza lo bhai! 😎"
    )


if __name__ == "__main__":
    smart_merge_memories()
