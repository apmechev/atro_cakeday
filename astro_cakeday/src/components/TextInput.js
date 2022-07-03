import React from "react";

const TextInput = ({value, changeHandler}) => {
  return (
    <div>
      <input
        type="text"
        value={value}
        onChange={changeHandler}
      />
      <p></p>
    </div>
  );
};

export default TextInput;
