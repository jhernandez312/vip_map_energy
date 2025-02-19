import { useEffect } from "react";

const ButtonComponent = () => {
    useEffect(() => {
        const handleClick = async () => {
            try {
                console.log("Sending API request...");

                const response = await fetch("http://localhost:5000/predict", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({
                        Building_Type: 1,
                        Building_Shape: 1,
                        Orientation: 1,
                        Building_Height: 1,
                        Building_Stories: 1,
                        Wall_Area: 1,
                        Window_Area: 1,
                        Roof_Area: 1,
                        energy_code: 1,
                        hvac_category: 1,
                    }),
                });

                if (!response.ok) {
                    throw new Error("Failed to get prediction from Flask API");
                }

                const result = await response.json();
                console.log("API Response:", result);

            } catch (error) {
                console.error("Error during API call:", error);
            }
        };

        const button = document.getElementById("hello-button");
        if (button) {
            button.addEventListener("click", handleClick);
        }

        return () => {
            if (button) {
                button.removeEventListener("click", handleClick);
            }
        };
    }, []);

    return null;
};

export default ButtonComponent;
