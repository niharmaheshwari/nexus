import NexusCard from "../../../../../core/components/nexusCard";
import "./style.css"

interface Props {
    description: string,
    tags: string[]
    onClick?: () => void
}

const SnippetCard = (props: Props) => {
    return (
        <div className="cardMain" onClick={props.onClick}>
            <NexusCard>
                <p>{props.description}</p>
                <ul>
                    {
                        props.tags.map((item, idx) => {
                            return <li key={idx+item}>{item}</li>
                        })
                    }
                </ul>
            </NexusCard>
        </div>
    );
}

export default SnippetCard;