card_css = """
        <head>
            <style>
                .card {
                    max-width: 80%;
                    margin-left: auto;
                    border: 1px solid #ccdbe9;
                    border-radius: 1rem;
                    overflow: hidden;
                    background-color: #445566;
                    padding: 1rem;
                    border-radius: 0.5rem;
                }
                .card:hover {
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.7);
                }
                .card-img {
                    width: 100%;
                    height: 200px;
                    object-fit: cover;
                    border-radius: 0.5rem;
                }
                .card-body {
                    padding: 10px;
                    flex-grow: 1;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    margin-top: 1rem;
                }
                .card-body h3 {
                    margin: 0;
                    font-size: 1.7em;
                    color: #ffffff;
                    font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
                    font-weight: bold;
                    line-height: 1.1;
                }
                .card a {
                    text-decoration: none;
                    color: #fff;
                }
                .card-body p {
                    color: #ccdbe9;
                    font-style: italic;
                }
                .ratings {
                    width: 50%;
                    display: grid;
                    grid-template-columns: repeat(3, 1fr);
                    gap: 1rem;
                }
                .badge {
                    display: inline-block;
                    padding: 0.5em;
                    font-size: 90%;
                    font-weight: bold;
                    line-height: 1;
                    text-align: center;
                    white-space: nowrap;
                    vertical-align: baseline;
                    border-radius: 0.25rem;
                }
                .badge-primary {
                    color: #fff;
                    background-color: #d69e02;
                }
                .badge-secondary {
                    color: #fff;
                    background-color: #a31702;
                }
                .badge-terciary {
                    color: #fff;
                    background-color: #212121;
                }
                @media (min-width: 1440px) {
                    .card {
                        max-width: 800px;
                        margin: 20px auto;
                    }
                    .card-img {
                        height: 325px;
                    }
                }
            </style>
        </head>

    """
    