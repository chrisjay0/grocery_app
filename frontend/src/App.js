import React, { useState } from "react";
import {
  Container,
  Divider,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  IconButton,
  Typography,
  Button,
  Box,
} from "@mui/material";
import CloseIcon from "@mui/icons-material/Close";
import ItemInput from "./ItemInput";
import PriceComparison from "./PriceComparison";
import axios from "axios";

const App = () => {
  const [items, setItems] = useState([]);
  const [currentItem, setCurrentItem] = useState("");
  const [showComparison, setShowComparison] = useState(false);

  const handleAddToList = async () => {
    if (currentItem.trim()) {
      // Optimistically update the state and clear the input
      setItems((prevItems) => [...prevItems, currentItem]);
      setCurrentItem("");

      try {
        await axios.post("http://127.0.0.1:5000/prices", {
          item_name: currentItem,
        });
        // If needed, handle any additional logic after the server responds successfully
      } catch (error) {
        // Handle the error if the server request fails
        // For example, you can revert the state update or show an error message to the user
        setItems((prevItems) =>
          prevItems.filter((item) => item !== currentItem)
        );
        alert("Failed to add item. Please try again.");
      }
    }
  };

  const handleRemoveItem = (indexToRemove) => {
    setItems((prevItems) =>
      prevItems.filter((_, index) => index !== indexToRemove)
    );
  };

  return (
    <Container
      maxWidth="lg"
      style={{
        display: "flex",
        justifyContent: showComparison ? "flex-start" : "center",
        alignItems: "flex-start",
        paddingTop: "10vh",
      }}
    >
      <div
        style={{
          marginLeft: showComparison ? "10rem" : "0rem",
          marginRight: showComparison ? "-10rem" : "0rem",
        }}
      >
        <Typography
          variant="h4"
          component="h1"
          align={showComparison ? "center" : "center"}
          gutterBottom
        >
          Grocery Price Comparator
        </Typography>
        <Box
          display="flex"
          flexDirection="column"
          alignItems={showComparison ? "" : "center"}
        >
          <ItemInput
            currentItem={currentItem}
            onItemChange={setCurrentItem}
            onAddItem={handleAddToList}
          />

          <Button
            variant="contained"
            color="primary"
            onClick={handleAddToList}
            style={{ marginTop: "0.5rem" }}
          >
            Add to List
          </Button>
          <Button
            variant="contained"
            color="secondary"
            onClick={() => setShowComparison(true)}
            disabled={items.length === 0}
            style={{ marginTop: "0.5rem" }}
          >
            Check Prices
          </Button>
        </Box>
        <List style={{ marginTop: "1rem" }}>
          {items.map((item, index) => (
            <ListItem key={index}>
              <ListItemText primary={item} />
              <ListItemSecondaryAction>
                <IconButton
                  edge="end"
                  aria-label="delete"
                  onClick={() => handleRemoveItem(index)}
                >
                  <CloseIcon />
                </IconButton>
              </ListItemSecondaryAction>
            </ListItem>
          ))}
        </List>
      </div>
      {showComparison && <PriceComparison items={items} />}
    </Container>
  );
};

export default App;
