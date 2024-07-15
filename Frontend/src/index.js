import React from "react";
import ReactDOM from "react-dom/client";
import { Widget } from 'react-chat-widget';
import 'react-chat-widget/lib/styles.css';

import App from "./App";

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
    <>
    <Widget />
    <App />
    </>
    );
